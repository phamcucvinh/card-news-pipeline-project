/**
 * ============================================================================
 * 적 클래스 (Enemy.js)
 * ============================================================================
 *
 * 목적: 개별 적(Enemy) 객체를 표현하고 동작을 관리합니다.
 *
 * 주요 책임:
 * 1. 적 우주선 3D 모델 생성 (팔면체 + 눈)
 * 2. 이동 패턴 구현 (사인파, 원형)
 * 3. 발사 타이밍 관리
 * 4. 체력 및 파괴 상태 관리
 * 5. 플레이어 향해 이동
 *
 * 디자인:
 * - 각 적은 독립적인 Entity 객체
 * - 웨이브에 따라 속도와 발사 빈도 증가
 * - 2가지 이동 패턴으로 다양성 제공
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';

export class Enemy {
    /**
     * 적 생성자
     *
     * @param {SceneManager} sceneManager - 씬 관리자 (의존성 주입)
     * @param {number} x - 생성 x 위치
     * @param {number} y - 생성 y 위치
     * @param {number} z - 생성 z 위치
     * @param {number} wave - 현재 웨이브 번호 (난이도 결정)
     */
    constructor(sceneManager, x, y, z, wave) {
        // 씬 관리자 참조
        this.sceneManager = sceneManager;

        // 적의 3D 메시 객체
        this.mesh = null;

        // 현재 웨이브 번호 (점수 계산에 사용)
        this.wave = wave;

        // 적의 체력
        this.health = CONFIG.ENEMY.HEALTH;

        // 적의 이동 속도 (웨이브가 높을수록 빨라짐)
        // 예: 웨이브 1 = 0.02, 웨이브 2 = 0.025, 웨이브 3 = 0.03...
        this.speed = CONFIG.ENEMY.BASE_SPEED + (wave * CONFIG.ENEMY.SPEED_INCREMENT);

        // 발사 타이머 (무작위 초기값으로 발사 시간 분산)
        this.shootTimer = Math.random() * CONFIG.ENEMY.SHOOT_INTERVAL_BASE;

        // 이동 패턴 무작위 선택 (50% 확률로 'sine' 또는 'circle')
        this.movementPattern = Math.random() > 0.5 ? 'sine' : 'circle';

        // 이동 패턴에 사용되는 시간 변수
        this.time = 0;

        // 적의 활성 상태 (false면 제거 대상)
        this.active = true;

        // 초기화 메서드 호출
        this.init(x, y, z);
    }

    /**
     * 초기화 메서드
     *
     * 적의 3D 메시를 생성하고 씬에 추가합니다.
     *
     * @param {number} x - 초기 x 위치
     * @param {number} y - 초기 y 위치
     * @param {number} z - 초기 z 위치
     */
    init(x, y, z) {
        // 적 메시 생성
        this.mesh = this.createMesh();

        // 위치 설정
        this.mesh.position.set(x, y, z);

        // 씬에 추가
        this.sceneManager.add(this.mesh);
    }

    /**
     * 적 메시 생성 메서드
     *
     * 팔면체 본체와 2개의 눈을 가진 적 우주선을 생성합니다.
     * Group을 사용하여 여러 메시를 하나로 묶습니다.
     *
     * @returns {THREE.Group} 적 우주선 그룹 객체
     */
    createMesh() {
        // 그룹 생성 (여러 메시를 하나로 묶음)
        const group = new THREE.Group();

        // 1. 적 본체 (팔면체 - Octahedron)
        const bodyGeometry = new THREE.OctahedronGeometry(CONFIG.ENEMY.SIZE);
        const bodyMaterial = new THREE.MeshPhongMaterial({
            color: CONFIG.ENEMY.COLOR,        // 빨간색
            emissive: CONFIG.ENEMY.COLOR,     // 발광 색상
            emissiveIntensity: 0.5,           // 발광 강도
            shininess: 100                     // 반짝임 정도
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        group.add(body);

        // 2. 적의 눈 생성
        const eyeGeometry = new THREE.SphereGeometry(0.15, 8, 8);
        const eyeMaterial = new THREE.MeshPhongMaterial({
            color: 0xffff00,              // 노란색
            emissive: 0xffff00,           // 발광 노란색
            emissiveIntensity: 1          // 최대 발광 (빛나는 눈 효과)
        });

        // 왼쪽 눈
        const eye1 = new THREE.Mesh(eyeGeometry, eyeMaterial);
        eye1.position.set(-0.3, 0.2, 0.5);  // 왼쪽 위 앞쪽에 배치
        group.add(eye1);

        // 오른쪽 눈
        const eye2 = new THREE.Mesh(eyeGeometry, eyeMaterial);
        eye2.position.set(0.3, 0.2, 0.5);   // 오른쪽 위 앞쪽에 배치
        group.add(eye2);

        // 완성된 그룹 반환
        return group;
    }

    /**
     * 적 업데이트 메서드
     *
     * 매 프레임마다 호출되어 적을 업데이트합니다.
     * 이동, 회전, 발사 타이머, 탈출 체크를 수행합니다.
     *
     * @returns {Object|null} 적이 탈출하면 객체 반환, 아니면 null
     */
    update() {
        // 비활성 상태면 아무것도 하지 않음
        if (!this.active) return;

        // 이동 패턴 업데이트
        this.updateMovement();

        // 회전 애니메이션
        this.updateRotation();

        // 발사 타이머 증가
        this.updateShootTimer();

        // 적이 플레이어를 통과했는지 확인
        // z > 15는 플레이어 뒤쪽을 의미
        if (this.mesh.position.z > 15) {
            // 적 비활성화
            this.active = false;

            // 탈출 정보 반환 (플레이어가 피해를 입음)
            return { escaped: true, damage: CONFIG.DAMAGE.ENEMY_COLLISION };
        }

        // 정상 상태
        return null;
    }

    /**
     * 이동 패턴 업데이트
     *
     * 선택된 이동 패턴에 따라 적을 이동시킵니다.
     * - sine: 사인파 패턴 (좌우로 물결치듯 이동)
     * - circle: 원형 패턴 (타원 궤도로 이동)
     */
    updateMovement() {
        // 시간 변수 증가 (이동 패턴 계산에 사용)
        this.time += 0.05;

        // 이동 패턴 적용
        if (this.movementPattern === 'sine') {
            // 사인파 패턴: x축으로 사인파 움직임
            // Math.sin(this.time)는 -1 ~ 1 범위
            // 0.1을 곱하면 좌우 이동 폭 결정
            this.mesh.position.x += Math.sin(this.time) * 0.1;

        } else {
            // 원형 패턴: 타원 궤도 이동
            // x축: 코사인 함수 (좌우)
            // y축: 사인 함수 (상하)
            // time * 0.5로 느린 회전 속도
            this.mesh.position.x = Math.cos(this.time * 0.5) * 8;  // 반지름 8
            this.mesh.position.y = Math.sin(this.time * 0.5) * 5;  // 반지름 5
        }

        // 플레이어를 향해 앞으로 이동 (z축 증가)
        this.mesh.position.z += this.speed;
    }

    /**
     * 회전 애니메이션 업데이트
     *
     * 적을 y축 기준으로 천천히 회전시킵니다.
     * 회전하는 적의 모습으로 역동감을 더합니다.
     */
    updateRotation() {
        // y축 기준 회전 (좌우 회전)
        this.mesh.rotation.y += 0.02;
    }

    /**
     * 발사 타이머 업데이트
     *
     * 발사 간격을 측정하기 위한 타이머를 증가시킵니다.
     */
    updateShootTimer() {
        this.shootTimer++;
    }

    /**
     * 발사 여부 판단 메서드
     *
     * 현재 발사해야 하는지 확인합니다.
     * 웨이브가 높을수록 발사 간격이 짧아집니다.
     *
     * @returns {boolean} true면 발사 시점
     */
    shouldShoot() {
        // 웨이브에 따른 발사 간격 계산
        // 웨이브가 높을수록 간격이 짧아짐
        // 예: 웨이브 1 = 100, 웨이브 2 = 95, 웨이브 3 = 90...
        const interval = CONFIG.ENEMY.SHOOT_INTERVAL_BASE -
                        (this.wave * CONFIG.ENEMY.SHOOT_INTERVAL_DECREMENT);

        // 타이머가 간격에 도달하면
        if (this.shootTimer >= interval) {
            // 타이머 리셋
            this.shootTimer = 0;

            // 발사!
            return true;
        }

        // 아직 발사 시점 아님
        return false;
    }

    /**
     * 적의 위치 반환 (Getter)
     *
     * @returns {THREE.Vector3} 적의 현재 위치
     */
    getPosition() {
        return this.mesh.position;
    }

    /**
     * 피해 입기 메서드
     *
     * 적이 총알에 맞았을 때 호출됩니다.
     * 체력을 감소시키고, 체력이 0 이하면 파괴됩니다.
     *
     * @param {number} amount - 받는 피해량
     * @returns {boolean} true면 적이 파괴됨
     */
    takeDamage(amount) {
        // 체력 감소
        this.health -= amount;

        // 체력이 0 이하면
        if (this.health <= 0) {
            // 적 비활성화
            this.active = false;

            // 파괴됨 (true 반환)
            return true;
        }

        // 아직 살아있음 (false 반환)
        return false;
    }

    /**
     * 활성 상태 확인 (Getter)
     *
     * @returns {boolean} true면 적이 활성 상태
     */
    isActive() {
        return this.active;
    }

    /**
     * 웨이브 번호 반환 (Getter)
     *
     * 점수 계산 시 사용됩니다.
     *
     * @returns {number} 이 적이 속한 웨이브 번호
     */
    getWave() {
        return this.wave;
    }

    /**
     * 적 파괴 메서드
     *
     * 씬에서 적을 제거하고 메모리를 정리합니다.
     * 게임 재시작이나 적 격파 시 호출됩니다.
     */
    destroy() {
        // 메시가 존재하면
        if (this.mesh) {
            // 씬에서 제거
            this.sceneManager.remove(this.mesh);

            // 참조 해제 (가비지 컬렉션 대상)
            this.mesh = null;
        }

        // 비활성화
        this.active = false;
    }

    /**
     * 메시 객체 반환 (Getter)
     *
     * @returns {THREE.Group} 적의 메시 그룹
     */
    getMesh() {
        return this.mesh;
    }
}
