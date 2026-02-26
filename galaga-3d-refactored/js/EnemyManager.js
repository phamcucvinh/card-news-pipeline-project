/**
 * ============================================================================
 * 적 관리자 (EnemyManager.js)
 * ============================================================================
 *
 * 목적: 게임의 모든 적(Enemy)을 생성하고 관리합니다.
 *
 * 주요 책임:
 * 1. 웨이브 시스템 관리 (적 생성)
 * 2. 모든 적 객체의 업데이트
 * 3. 적 제거 및 생명주기 관리
 * 4. 난이도 증가 (웨이브마다 적 수 증가)
 * 5. 적의 발사 및 탈출 이벤트 수집
 *
 * 디자인 패턴: 관리자 패턴 (Manager Pattern)
 * - 개별 Enemy 객체를 생성하고 배열로 관리
 * - 일괄 업데이트 및 필터링 제공
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';
import { Enemy } from './Enemy.js';

export class EnemyManager {
    /**
     * 적 관리자 생성자
     *
     * @param {SceneManager} sceneManager - 씬 관리자 (의존성 주입)
     */
    constructor(sceneManager) {
        // 씬 관리자 참조 (적을 씬에 추가/제거하기 위함)
        this.sceneManager = sceneManager;

        // 현재 활성화된 모든 적 객체의 배열
        this.enemies = [];

        // 현재 웨이브 번호 (1부터 시작)
        this.currentWave = 1;

        // 이번 웨이브에 생성할 적의 수
        this.enemiesPerWave = CONFIG.WAVE.INITIAL_ENEMIES;
    }

    /**
     * 웨이브 생성 메서드
     *
     * 현재 웨이브에 맞는 수의 적을 생성합니다.
     * 적들은 설정된 스폰 존 내의 무작위 위치에 생성됩니다.
     *
     * 스폰 알고리즘:
     * - x, y: 중앙을 기준으로 범위 내 무작위
     * - z: 화면 앞쪽에서 일정 깊이 범위 내 무작위
     */
    spawnWave() {
        // 스폰 존 설정 가져오기
        const zone = CONFIG.ENEMY.SPAWN_ZONE;

        // 설정된 수만큼 적 생성
        for (let i = 0; i < this.enemiesPerWave; i++) {
            // 무작위 x 위치 계산
            // (Math.random() - 0.5)는 -0.5 ~ 0.5 범위
            // zone.X_RANGE를 곱하면 -7.5 ~ 7.5 범위
            const x = (Math.random() - 0.5) * zone.X_RANGE;

            // 무작위 y 위치 계산 (상하)
            const y = (Math.random() - 0.5) * zone.Y_RANGE;

            // 무작위 z 위치 계산 (깊이)
            // Z_START는 음수 (화면 앞쪽)
            // Z_RANGE만큼 더 앞으로 배치
            const z = zone.Z_START - Math.random() * zone.Z_RANGE;

            // 새로운 적 객체 생성
            const enemy = new Enemy(
                this.sceneManager,  // 씬 관리자
                x, y, z,           // 위치
                this.currentWave   // 현재 웨이브 번호 (난이도 결정)
            );

            // 적 배열에 추가
            this.enemies.push(enemy);
        }
    }

    /**
     * 모든 적 업데이트 메서드
     *
     * 매 프레임마다 호출되어 모든 적을 업데이트합니다.
     * 탈출한 적은 제거하고, 발사할 적의 정보를 수집합니다.
     *
     * @returns {Object} 업데이트 결과 객체
     *   - escaped: 탈출한 적의 정보 배열 [{escaped: true, damage: 10}]
     *   - shouldShoot: 발사할 적의 위치 배열 [Vector3, Vector3, ...]
     */
    update() {
        // 결과를 담을 객체 초기화
        const results = {
            escaped: [],      // 플레이어를 통과한 적들
            shouldShoot: []   // 발사할 적들의 위치
        };

        // 모든 적 업데이트 및 필터링
        // filter는 조건에 맞는 요소만 남김 (false 반환 시 제거)
        this.enemies = this.enemies.filter(enemy => {
            // 각 적의 update 메서드 호출
            const updateResult = enemy.update();

            // 적이 플레이어를 통과했는지 확인
            if (updateResult && updateResult.escaped) {
                // 적 제거
                enemy.destroy();

                // 탈출 정보를 결과에 추가
                results.escaped.push(updateResult);

                // 배열에서 제거 (false 반환)
                return false;
            }

            // 적이 발사해야 하는지 확인
            if (enemy.shouldShoot()) {
                // 적의 현재 위치를 복사하여 저장
                // clone()을 사용하여 참조가 아닌 새 객체 생성
                results.shouldShoot.push(enemy.getPosition().clone());
            }

            // 적이 여전히 활성 상태인지 확인
            // 활성 상태면 배열에 유지 (true 반환)
            return enemy.isActive();
        });

        // 업데이트 결과 반환
        return results;
    }

    /**
     * 모든 적 배열 반환 (Getter)
     *
     * @returns {Enemy[]} 현재 활성화된 모든 적의 배열
     */
    getEnemies() {
        return this.enemies;
    }

    /**
     * 특정 적 제거 메서드
     *
     * 충돌이나 격파 등으로 적을 즉시 제거할 때 사용합니다.
     *
     * @param {Enemy} enemy - 제거할 적 객체
     */
    removeEnemy(enemy) {
        // 배열에서 적의 인덱스 찾기
        const index = this.enemies.indexOf(enemy);

        // 적이 배열에 존재하면
        if (index > -1) {
            // 적 파괴 (씬에서 제거)
            enemy.destroy();

            // 배열에서 제거
            // splice(인덱스, 제거할개수)
            this.enemies.splice(index, 1);
        }
    }

    /**
     * 적 존재 여부 확인
     *
     * 웨이브 클리어 조건을 확인할 때 사용합니다.
     *
     * @returns {boolean} true면 적이 없음 (웨이브 클리어)
     */
    isEmpty() {
        return this.enemies.length === 0;
    }

    /**
     * 다음 웨이브로 진행
     *
     * 웨이브 번호를 증가시키고, 생성할 적의 수를 늘립니다.
     * 게임 난이도가 점진적으로 증가합니다.
     */
    nextWave() {
        // 웨이브 번호 1 증가
        this.currentWave++;

        // 웨이브당 적 수 증가
        // 예: 5 → 7 → 9 → 11...
        this.enemiesPerWave += CONFIG.WAVE.ENEMY_INCREMENT;
    }

    /**
     * 현재 웨이브 번호 반환 (Getter)
     *
     * @returns {number} 현재 웨이브 번호
     */
    getCurrentWave() {
        return this.currentWave;
    }

    /**
     * 리셋 메서드
     *
     * 게임 재시작 시 모든 적을 제거하고 초기 상태로 돌아갑니다.
     */
    reset() {
        // 모든 적 파괴 (씬에서 제거)
        this.enemies.forEach(enemy => enemy.destroy());

        // 적 배열 비우기
        this.enemies = [];

        // 웨이브 번호 초기화
        this.currentWave = 1;

        // 적 수 초기화
        this.enemiesPerWave = CONFIG.WAVE.INITIAL_ENEMIES;
    }

    /**
     * 현재 적의 수 반환
     *
     * @returns {number} 현재 화면에 있는 적의 수
     */
    getCount() {
        return this.enemies.length;
    }
}
