/**
 * ============================================================================
 * 총알 관리자 (BulletManager.js)
 * ============================================================================
 *
 * 목적: 게임의 모든 총알(Bullet)을 생성하고 관리합니다.
 *
 * 주요 책임:
 * 1. 플레이어 총알 생성 및 관리
 * 2. 적 총알 생성 및 관리
 * 3. 총알 이동 및 애니메이션
 * 4. 화면 밖 총알 자동 제거 (메모리 최적화)
 * 5. 충돌 시 총알 제거
 *
 * 디자인:
 * - 플레이어와 적의 총알을 별도 배열로 관리
 * - Three.js Mesh 객체에 메타데이터 저장 (userData)
 * - 발광 효과(glow) 추가로 시각적 효과 강화
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';

export class BulletManager {
    /**
     * 총알 관리자 생성자
     *
     * @param {SceneManager} sceneManager - 씬 관리자 (의존성 주입)
     */
    constructor(sceneManager) {
        // 씬 관리자 참조
        this.sceneManager = sceneManager;

        // 플레이어가 발사한 총알 배열
        this.playerBullets = [];

        // 적이 발사한 총알 배열
        this.enemyBullets = [];
    }

    /**
     * 총알 생성 메서드 (팩토리 메서드)
     *
     * 플레이어 또는 적의 총알을 생성합니다.
     * 총알은 구체(Sphere) 형태에 발광 효과가 추가됩니다.
     *
     * @param {number} x - 총알 생성 x 위치
     * @param {number} y - 총알 생성 y 위치
     * @param {number} z - 총알 생성 z 위치
     * @param {boolean} isPlayer - true면 플레이어 총알, false면 적 총알
     * @returns {THREE.Mesh} 생성된 총알 메시 객체
     */
    createBullet(x, y, z, isPlayer = true) {
        // 총알 종류에 따른 설정 선택
        const config = isPlayer ? CONFIG.BULLET.PLAYER : CONFIG.BULLET.ENEMY;

        // 1. 총알 본체 생성
        // 구체 기하학 (반지름, 가로 세그먼트, 세로 세그먼트)
        const geometry = new THREE.SphereGeometry(config.SIZE, 8, 8);

        // 퐁 재질 (빛을 반사하는 재질)
        const material = new THREE.MeshPhongMaterial({
            color: config.COLOR,              // 기본 색상
            emissive: config.COLOR,           // 발광 색상 (스스로 빛을 냄)
            emissiveIntensity: 1              // 발광 강도 (최대)
        });

        // 메시 생성 (기하학 + 재질)
        const bullet = new THREE.Mesh(geometry, material);

        // 총알 위치 설정
        bullet.position.set(x, y, z);

        // 2. 발광 효과(Glow) 추가
        // 총알보다 1.7배 큰 반투명 구체를 추가하여 후광 효과 생성
        const glowGeometry = new THREE.SphereGeometry(config.SIZE * 1.7, 8, 8);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: config.COLOR,     // 발광 색상
            transparent: true,       // 투명도 활성화
            opacity: 0.3            // 30% 불투명도 (70% 투명)
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);

        // 발광 효과를 총알에 자식으로 추가
        // 총알이 이동하면 발광 효과도 함께 이동
        bullet.add(glow);

        // 3. 씬에 총알 추가
        this.sceneManager.add(bullet);

        // 4. 총알 메타데이터 저장
        // userData는 Three.js 객체에 커스텀 데이터를 저장하는 표준 방법
        bullet.userData = {
            speed: config.SPEED,      // 이동 속도
            isPlayer: isPlayer        // 플레이어 총알 여부
        };

        // 생성된 총알 반환
        return bullet;
    }

    /**
     * 플레이어 총알 발사
     *
     * 플레이어의 현재 위치에서 총알을 발사합니다.
     * 총알은 플레이어보다 약간 앞쪽에서 생성됩니다.
     *
     * @param {THREE.Vector3} position - 플레이어의 현재 위치
     */
    shootPlayerBullet(position) {
        // 총알 생성 (플레이어 위치에서 z-1만큼 앞쪽)
        const bullet = this.createBullet(
            position.x,          // 플레이어 x 위치
            position.y,          // 플레이어 y 위치
            position.z - 1,      // 플레이어보다 1 앞쪽
            true                 // 플레이어 총알
        );

        // 플레이어 총알 배열에 추가
        this.playerBullets.push(bullet);
    }

    /**
     * 적 총알 발사
     *
     * 적의 현재 위치에서 총알을 발사합니다.
     *
     * @param {THREE.Vector3} position - 적의 현재 위치
     */
    shootEnemyBullet(position) {
        // 총알 생성 (적의 위치)
        const bullet = this.createBullet(
            position.x,          // 적 x 위치
            position.y,          // 적 y 위치
            position.z,          // 적 z 위치
            false                // 적 총알
        );

        // 적 총알 배열에 추가
        this.enemyBullets.push(bullet);
    }

    /**
     * 모든 총알 업데이트 메서드
     *
     * 매 프레임마다 호출되어 모든 총알을 업데이트합니다.
     */
    update() {
        this.updatePlayerBullets();
        this.updateEnemyBullets();
    }

    /**
     * 플레이어 총알 업데이트
     *
     * 플레이어 총알을 앞으로 이동시키고,
     * 화면 밖으로 나간 총알은 제거합니다.
     */
    updatePlayerBullets() {
        // 필터 함수: 조건을 만족하는 총알만 배열에 유지
        this.playerBullets = this.playerBullets.filter(bullet => {
            // 총알을 앞으로 이동 (z값 감소 = 화면 앞쪽으로)
            bullet.position.z -= bullet.userData.speed;

            // 총알 회전 애니메이션 (x축 기준 회전)
            bullet.rotation.x += 0.1;

            // 총알이 너무 멀리 나갔는지 확인
            if (bullet.position.z < -CONFIG.BULLET.MAX_DISTANCE) {
                // 씬에서 총알 제거
                this.sceneManager.remove(bullet);

                // 배열에서 제거 (false 반환)
                return false;
            }

            // 총알 유지 (true 반환)
            return true;
        });
    }

    /**
     * 적 총알 업데이트
     *
     * 적 총알을 플레이어 방향(뒤쪽)으로 이동시키고,
     * 화면 밖으로 나간 총알은 제거합니다.
     */
    updateEnemyBullets() {
        // 필터 함수: 조건을 만족하는 총알만 배열에 유지
        this.enemyBullets = this.enemyBullets.filter(bullet => {
            // 총알을 뒤로 이동 (z값 증가 = 플레이어 방향)
            bullet.position.z += bullet.userData.speed;

            // 총알 회전 애니메이션
            bullet.rotation.x += 0.1;

            // 총알이 플레이어 뒤쪽으로 너무 멀리 갔는지 확인
            if (bullet.position.z > CONFIG.BULLET.MAX_DISTANCE) {
                // 씬에서 총알 제거
                this.sceneManager.remove(bullet);

                // 배열에서 제거 (false 반환)
                return false;
            }

            // 총알 유지 (true 반환)
            return true;
        });
    }

    /**
     * 특정 총알 제거 메서드
     *
     * 충돌 감지 등으로 특정 총알을 즉시 제거할 때 사용합니다.
     *
     * @param {THREE.Mesh} bullet - 제거할 총알 객체
     * @param {boolean} isPlayerBullet - 플레이어 총알이면 true
     */
    removeBullet(bullet, isPlayerBullet) {
        // 총알 종류에 따라 배열 선택
        const array = isPlayerBullet ? this.playerBullets : this.enemyBullets;

        // 배열에서 총알의 인덱스 찾기
        const index = array.indexOf(bullet);

        // 총알이 배열에 존재하면
        if (index > -1) {
            // 씬에서 총알 제거
            this.sceneManager.remove(bullet);

            // 배열에서 총알 제거
            // splice(시작인덱스, 제거개수)
            array.splice(index, 1);
        }
    }

    /**
     * 플레이어 총알 배열 반환 (Getter)
     *
     * @returns {THREE.Mesh[]} 플레이어 총알 배열
     */
    getPlayerBullets() {
        return this.playerBullets;
    }

    /**
     * 적 총알 배열 반환 (Getter)
     *
     * @returns {THREE.Mesh[]} 적 총알 배열
     */
    getEnemyBullets() {
        return this.enemyBullets;
    }

    /**
     * 리셋 메서드
     *
     * 게임 재시작 시 모든 총알을 제거합니다.
     * 메모리 누수 방지를 위해 씬과 배열에서 모두 제거합니다.
     */
    reset() {
        // 모든 플레이어 총알 제거
        this.playerBullets.forEach(bullet => {
            this.sceneManager.remove(bullet);
        });
        // 플레이어 총알 배열 초기화
        this.playerBullets = [];

        // 모든 적 총알 제거
        this.enemyBullets.forEach(bullet => {
            this.sceneManager.remove(bullet);
        });
        // 적 총알 배열 초기화
        this.enemyBullets = [];
    }
}
