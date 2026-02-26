/**
 * ============================================================================
 * 플레이어 클래스 (Player.js)
 * ============================================================================
 *
 * 목적: 플레이어 우주선을 표현하고 조작을 관리합니다.
 *
 * 주요 책임:
 * 1. 플레이어 우주선 3D 모델 생성 (피라미드, 날개, 조종석)
 * 2. 키보드 입력 처리 (WASD, 방향키)
 * 3. 이동 및 경계 제한
 * 4. 발사 쿨다운 관리
 * 5. 체력 및 피격 처리
 * 6. 이동에 따른 회전 애니메이션
 *
 * 디자인:
 * - 사용자 입력을 직접 처리 (키 상태 저장)
 * - 경계 검사로 화면 밖으로 나가지 않도록 제한
 * - 쿨다운 시스템으로 연사 속도 제어
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';

export class Player {
    /**
     * 플레이어 생성자
     *
     * @param {SceneManager} sceneManager - 씬 관리자 (의존성 주입)
     */
    constructor(sceneManager) {
        // 씬 관리자 참조
        this.sceneManager = sceneManager;

        // 플레이어의 3D 메시 객체
        this.mesh = null;

        // 플레이어 체력
        this.health = CONFIG.PLAYER.START_HEALTH;

        // 키 상태를 저장하는 객체
        // 예: { 'w': true, 'a': false, ... }
        this.keys = {};

        // 마지막 발사 시간 (밀리초)
        this.lastShootTime = 0;

        // 초기화 메서드 호출
        this.init();

        // 키보드 이벤트 리스너 설정
        this.setupEventListeners();
    }

    /**
     * 초기화 메서드
     *
     * 플레이어 메시를 생성하고 초기 위치에 배치합니다.
     */
    init() {
        // 플레이어 메시 생성
        this.mesh = this.createMesh();

        // 초기 위치 설정
        const pos = CONFIG.PLAYER.START_POSITION;
        this.mesh.position.set(pos.x, pos.y, pos.z);

        // 씬에 추가
        this.sceneManager.add(this.mesh);
    }

    /**
     * 플레이어 메시 생성 메서드
     *
     * 피라미드 형태의 본체, 날개, 조종석으로 구성된
     * 플레이어 우주선을 생성합니다.
     *
     * @returns {THREE.Group} 플레이어 우주선 그룹 객체
     */
    createMesh() {
        // 그룹 생성 (여러 부품을 하나로 묶음)
        const group = new THREE.Group();

        // 1. 본체 (피라미드 - 역방향 원뿔)
        const bodyGeometry = new THREE.ConeGeometry(
            CONFIG.PLAYER.SIZE.radius,    // 반지름
            CONFIG.PLAYER.SIZE.height,    // 높이
            4                             // 세그먼트 (4 = 피라미드)
        );
        const bodyMaterial = new THREE.MeshPhongMaterial({
            color: CONFIG.PLAYER.COLOR,          // 녹색
            emissive: CONFIG.PLAYER.COLOR,       // 발광 녹색
            emissiveIntensity: 0.5,              // 발광 강도
            shininess: 100                        // 반짝임
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);

        // 피라미드를 뒤집기 (끝이 앞을 향하도록)
        body.rotation.x = Math.PI;

        group.add(body);

        // 2. 날개
        const wingGeometry = new THREE.BoxGeometry(2, 0.1, 0.5);
        const wingMaterial = new THREE.MeshPhongMaterial({
            color: 0x00aa00,              // 어두운 녹색
            emissive: 0x00aa00,           // 발광 어두운 녹색
            emissiveIntensity: 0.3        // 약한 발광
        });
        const wings = new THREE.Mesh(wingGeometry, wingMaterial);

        // 날개 위치 (본체 아래쪽)
        wings.position.y = -0.3;

        group.add(wings);

        // 3. 조종석 (구체)
        const cockpitGeometry = new THREE.SphereGeometry(0.3, 16, 16);
        const cockpitMaterial = new THREE.MeshPhongMaterial({
            color: 0x00ffff,              // 청록색 (시안)
            emissive: 0x00ffff,           // 발광 청록색
            emissiveIntensity: 0.8,       // 강한 발광
            transparent: true,            // 투명도 활성화
            opacity: 0.9                  // 90% 불투명 (약간 투명)
        });
        const cockpit = new THREE.Mesh(cockpitGeometry, cockpitMaterial);

        // 조종석 위치 (본체 위쪽)
        cockpit.position.y = 0.3;

        group.add(cockpit);

        // 완성된 플레이어 우주선 반환
        return group;
    }

    /**
     * 키보드 이벤트 리스너 설정
     *
     * keydown, keyup 이벤트를 감지하여 keys 객체에 키 상태를 저장합니다.
     * 이 방식은 여러 키를 동시에 누르는 것을 지원합니다.
     */
    setupEventListeners() {
        // 키를 눌렀을 때
        document.addEventListener('keydown', (e) => {
            // 키 이름을 소문자로 변환하여 저장
            // 예: 'W' → 'w', 'ArrowUp' → 'arrowup'
            this.keys[e.key.toLowerCase()] = true;
        });

        // 키를 뗐을 때
        document.addEventListener('keyup', (e) => {
            // 키 상태를 false로 변경
            this.keys[e.key.toLowerCase()] = false;
        });
    }

    /**
     * 플레이어 업데이트 메서드
     *
     * 매 프레임마다 호출되어 플레이어를 업데이트합니다.
     * 이동과 회전 애니메이션을 처리합니다.
     */
    update() {
        // 메시가 존재하지 않으면 아무것도 하지 않음
        if (!this.mesh) return;

        // 키 입력에 따른 이동 처리
        this.handleMovement();

        // 이동에 따른 회전 업데이트
        this.updateRotation();
    }

    /**
     * 이동 처리 메서드
     *
     * 키 상태를 확인하여 플레이어를 이동시킵니다.
     * 화면 경계를 벗어나지 않도록 제한합니다.
     */
    handleMovement() {
        // 설정에서 이동 속도와 경계 가져오기
        const speed = CONFIG.PLAYER.SPEED;
        const bounds = CONFIG.PLAYER.BOUNDS;

        // 수직 이동 (상하)
        // W 또는 위 방향키를 누르면 위로 이동
        if (this.keys['w'] || this.keys['arrowup']) {
            // 새 위치 계산 후 최대값 제한
            // Math.min으로 상단 경계를 넘지 않도록 함
            this.mesh.position.y = Math.min(
                this.mesh.position.y + speed,  // 새 위치
                bounds.Y_MAX                   // 최대 y 값
            );
        }

        // S 또는 아래 방향키를 누르면 아래로 이동
        if (this.keys['s'] || this.keys['arrowdown']) {
            // Math.max로 하단 경계를 넘지 않도록 함
            this.mesh.position.y = Math.max(
                this.mesh.position.y - speed,  // 새 위치
                bounds.Y_MIN                   // 최소 y 값
            );
        }

        // 수평 이동 (좌우)
        // A 또는 왼쪽 방향키를 누르면 왼쪽으로 이동
        if (this.keys['a'] || this.keys['arrowleft']) {
            // Math.max로 왼쪽 경계를 넘지 않도록 함
            this.mesh.position.x = Math.max(
                this.mesh.position.x - speed,  // 새 위치
                bounds.X_MIN                   // 최소 x 값
            );
        }

        // D 또는 오른쪽 방향키를 누르면 오른쪽으로 이동
        if (this.keys['d'] || this.keys['arrowright']) {
            // Math.min으로 오른쪽 경계를 넘지 않도록 함
            this.mesh.position.x = Math.min(
                this.mesh.position.x + speed,  // 새 위치
                bounds.X_MAX                   // 최대 x 값
            );
        }
    }

    /**
     * 회전 애니메이션 업데이트
     *
     * 플레이어의 위치에 따라 자연스러운 회전 효과를 줍니다.
     * - 좌우 이동: z축 회전 (뱅킹 효과)
     * - 상하 이동: x축 회전 (피치 효과)
     */
    updateRotation() {
        // z축 회전 (좌우 뱅킹)
        // 왼쪽으로 이동하면 왼쪽으로 기울고, 오른쪽으로 이동하면 오른쪽으로 기울음
        // 음수를 곱해서 이동 방향과 같은 방향으로 기울도록 함
        this.mesh.rotation.z = -this.mesh.position.x * 0.05;

        // x축 회전 (상하 피치)
        // 위로 이동하면 약간 위를 향하고, 아래로 이동하면 약간 아래를 향함
        // Y_MAX에서 뺀 값을 사용하여 회전 방향 결정
        this.mesh.rotation.x = (this.mesh.position.y - CONFIG.PLAYER.BOUNDS.Y_MAX) * 0.05;
    }

    /**
     * 발사 가능 여부 확인 메서드
     *
     * 쿨다운 시간이 지났는지 확인합니다.
     * 연사 속도를 제어하여 게임 밸런스를 유지합니다.
     *
     * @returns {boolean} true면 발사 가능
     */
    canShoot() {
        // 현재 시간 (밀리초)
        const currentTime = Date.now();

        // 마지막 발사 이후 쿨다운 시간이 지났는지 확인
        if (currentTime - this.lastShootTime >= CONFIG.PLAYER.SHOOT_COOLDOWN) {
            // 마지막 발사 시간 업데이트
            this.lastShootTime = currentTime;

            // 발사 가능
            return true;
        }

        // 아직 쿨다운 중
        return false;
    }

    /**
     * 스페이스바 눌림 여부 확인
     *
     * @returns {boolean} 스페이스바가 눌려있으면 true
     */
    isShootKeyPressed() {
        return this.keys[' '];
    }

    /**
     * 플레이어 위치 반환 (Getter)
     *
     * @returns {THREE.Vector3} 플레이어의 현재 위치
     */
    getPosition() {
        return this.mesh.position;
    }

    /**
     * 피해 입기 메서드
     *
     * 플레이어가 적 총알에 맞았을 때 호출됩니다.
     * 체력을 감소시키고 피격 시각 효과를 표시합니다.
     *
     * @param {number} amount - 받는 피해량
     * @returns {number} 남은 체력
     */
    takeDamage(amount) {
        // 체력 감소
        this.health -= amount;

        // 피격 시각 효과 (깜빡임)
        this.flashOnHit();

        // 남은 체력 반환
        return this.health;
    }

    /**
     * 피격 시 깜빡임 효과
     *
     * 플레이어가 피해를 입었을 때 잠깐 밝게 빛나는 효과를 줍니다.
     * 시각적 피드백으로 플레이어가 피해를 인지할 수 있게 합니다.
     */
    flashOnHit() {
        // 설정에서 효과 정보 가져오기
        const effect = CONFIG.EFFECTS.PLAYER_HIT_FLASH;

        // 본체의 발광 강도를 최대로 올림
        // children[0]는 피라미드 본체
        this.mesh.children[0].material.emissiveIntensity = effect.INTENSITY;

        // 일정 시간 후 원래대로 복구
        setTimeout(() => {
            // 메시가 아직 존재하는지 확인 (게임 오버 등으로 제거될 수 있음)
            if (this.mesh) {
                // 발광 강도를 원래대로
                this.mesh.children[0].material.emissiveIntensity = 0.5;
            }
        }, effect.DURATION);
    }

    /**
     * 체력 반환 (Getter)
     *
     * @returns {number} 현재 체력
     */
    getHealth() {
        return this.health;
    }

    /**
     * 플레이어 파괴 메서드
     *
     * 게임 오버나 재시작 시 플레이어를 씬에서 제거합니다.
     * 메모리 누수를 방지하기 위해 참조도 해제합니다.
     */
    destroy() {
        // 메시가 존재하면
        if (this.mesh) {
            // 씬에서 제거
            this.sceneManager.remove(this.mesh);

            // 참조 해제 (가비지 컬렉션 대상)
            this.mesh = null;
        }
    }

    /**
     * 메시 객체 반환 (Getter)
     *
     * @returns {THREE.Group} 플레이어의 메시 그룹
     */
    getMesh() {
        return this.mesh;
    }
}
