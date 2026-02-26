/**
 * ============================================================================
 * 충돌 관리자 (CollisionManager.js)
 * ============================================================================
 *
 * 목적: 게임 내 모든 충돌을 감지하고 처리합니다.
 *
 * 주요 책임:
 * 1. 플레이어 총알 vs 적 충돌 감지
 * 2. 적 총알 vs 플레이어 충돌 감지
 * 3. 충돌 시 점수, 피해, 폭발 이벤트 수집
 * 4. 폭발 애니메이션 생성 및 재생
 *
 * 충돌 감지 알고리즘:
 * - 거리 기반 충돌 (Distance-based collision)
 * - 3D 공간에서 두 객체 간의 거리 계산
 * - 설정된 임계값보다 가까우면 충돌로 판정
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';

export class CollisionManager {
    /**
     * 충돌 관리자 생성자
     *
     * @param {SceneManager} sceneManager - 씬 관리자 (폭발 효과 추가용)
     */
    constructor(sceneManager) {
        // 씬 관리자 참조
        this.sceneManager = sceneManager;
    }

    /**
     * 모든 충돌 확인 메서드
     *
     * 매 프레임마다 호출되어 게임 내 모든 충돌을 검사합니다.
     * 검사 결과를 취합하여 반환합니다.
     *
     * @param {Player} player - 플레이어 객체
     * @param {EnemyManager} enemyManager - 적 관리자
     * @param {BulletManager} bulletManager - 총알 관리자
     * @returns {Object} 충돌 결과 객체
     *   - score: 획득한 점수
     *   - playerDamage: 플레이어가 받은 피해
     *   - explosions: 폭발 위치 배열
     */
    checkCollisions(player, enemyManager, bulletManager) {
        // 결과를 담을 객체 초기화
        const results = {
            score: 0,              // 이번 프레임에 획득한 점수
            playerDamage: 0,       // 플레이어가 받은 총 피해
            explosions: []         // 폭발이 일어날 위치들
        };

        // 1. 플레이어 총알 vs 적 충돌 검사
        this.checkPlayerBulletsVsEnemies(
            bulletManager.getPlayerBullets(),  // 플레이어 총알 배열
            enemyManager.getEnemies(),         // 적 배열
            bulletManager,                     // 총알 관리자 (총알 제거용)
            enemyManager,                      // 적 관리자 (적 제거용)
            results                            // 결과 객체 (수정됨)
        );

        // 2. 적 총알 vs 플레이어 충돌 검사
        this.checkEnemyBulletsVsPlayer(
            bulletManager.getEnemyBullets(),   // 적 총알 배열
            player,                            // 플레이어 객체
            bulletManager,                     // 총알 관리자
            results                            // 결과 객체 (수정됨)
        );

        // 충돌 검사 결과 반환
        return results;
    }

    /**
     * 플레이어 총알 vs 적 충돌 검사
     *
     * 모든 플레이어 총알과 모든 적을 순회하며 충돌을 확인합니다.
     * 충돌 시 총알 제거, 적 피해, 점수 증가, 폭발 효과를 처리합니다.
     *
     * 시간 복잡도: O(bullets * enemies)
     * 최적화 여지: 공간 분할(Spatial Partitioning) 알고리즘 적용 가능
     *
     * @param {THREE.Mesh[]} bullets - 플레이어 총알 배열
     * @param {Enemy[]} enemies - 적 배열
     * @param {BulletManager} bulletManager - 총알 관리자
     * @param {EnemyManager} enemyManager - 적 관리자
     * @param {Object} results - 결과 객체 (참조로 수정됨)
     */
    checkPlayerBulletsVsEnemies(bullets, enemies, bulletManager, enemyManager, results) {
        // 모든 플레이어 총알 순회
        bullets.forEach(bullet => {
            // 각 총알에 대해 모든 적 순회
            enemies.forEach(enemy => {
                // 거리 기반 충돌 감지
                // distanceTo: 3D 공간에서 두 점 사이의 유클리드 거리 계산
                // 공식: √((x2-x1)² + (y2-y1)² + (z2-z1)²)
                const distance = bullet.position.distanceTo(enemy.getPosition());

                // 거리가 임계값보다 작으면 충돌
                if (distance < CONFIG.COLLISION.BULLET_ENEMY_DISTANCE) {
                    // 적에게 피해 입힘 (1데미지)
                    // destroyed: 적이 파괴되었으면 true
                    const destroyed = enemy.takeDamage(1);

                    // 총알 제거 (관통하지 않음)
                    bulletManager.removeBullet(bullet, true);

                    // 적이 파괴되었으면
                    if (destroyed) {
                        // 폭발 위치 저장 (적의 위치 복사)
                        // clone()으로 새 객체 생성 (원본 보호)
                        results.explosions.push(enemy.getPosition().clone());

                        // 점수 계산
                        // 기본 점수 × 웨이브 승수
                        const scoreValue = CONFIG.SCORE.ENEMY_KILL_BASE *
                            (CONFIG.SCORE.WAVE_MULTIPLIER ? enemy.getWave() : 1);

                        // 점수 추가
                        results.score += scoreValue;

                        // 적 제거
                        enemyManager.removeEnemy(enemy);
                    }
                }
            });
        });
    }

    /**
     * 적 총알 vs 플레이어 충돌 검사
     *
     * 모든 적 총알과 플레이어의 충돌을 확인합니다.
     * 충돌 시 총알 제거와 플레이어 피해를 처리합니다.
     *
     * @param {THREE.Mesh[]} bullets - 적 총알 배열
     * @param {Player} player - 플레이어 객체
     * @param {BulletManager} bulletManager - 총알 관리자
     * @param {Object} results - 결과 객체 (참조로 수정됨)
     */
    checkEnemyBulletsVsPlayer(bullets, player, bulletManager, results) {
        // 플레이어나 메시가 없으면 검사하지 않음
        // 게임 오버나 초기화 중일 수 있음
        if (!player || !player.getMesh()) return;

        // 플레이어 위치 가져오기 (매번 호출하지 않도록 캐싱)
        const playerPosition = player.getPosition();

        // 모든 적 총알 순회
        bullets.forEach(bullet => {
            // 총알과 플레이어 사이의 거리 계산
            const distance = bullet.position.distanceTo(playerPosition);

            // 거리가 임계값보다 작으면 충돌
            if (distance < CONFIG.COLLISION.BULLET_PLAYER_DISTANCE) {
                // 총알 제거
                // 두 번째 인자 false = 적 총알
                bulletManager.removeBullet(bullet, false);

                // 플레이어 피해 누적
                results.playerDamage += CONFIG.DAMAGE.ENEMY_BULLET;
            }
        });
    }

    /**
     * 폭발 효과 생성 메서드
     *
     * 주어진 위치에 폭발 애니메이션을 생성합니다.
     * 구체가 점점 커지면서 투명해지는 효과를 만듭니다.
     *
     * @param {THREE.Vector3} position - 폭발이 일어날 위치
     */
    createExplosion(position) {
        // 폭발 효과 설정 가져오기
        const effect = CONFIG.EFFECTS.EXPLOSION;

        // 폭발 기하학 (구체)
        const geometry = new THREE.SphereGeometry(1, 16, 16);

        // 폭발 재질 (발광 재질)
        const material = new THREE.MeshBasicMaterial({
            color: effect.COLOR,     // 주황색
            transparent: true,       // 투명도 활성화
            opacity: 1               // 처음에는 불투명
        });

        // 폭발 메시 생성
        const explosion = new THREE.Mesh(geometry, material);

        // 폭발 위치 설정 (적이 있던 위치)
        explosion.position.copy(position);

        // 씬에 추가
        this.sceneManager.add(explosion);

        // 폭발 애니메이션 시작
        this.animateExplosion(explosion);
    }

    /**
     * 폭발 애니메이션 메서드
     *
     * 폭발 효과를 애니메이션합니다.
     * - 크기: 0에서 MAX_SCALE까지 점진적 증가
     * - 투명도: 1(불투명)에서 0(투명)까지 점진적 감소
     *
     * requestAnimationFrame을 사용한 재귀적 애니메이션입니다.
     *
     * @param {THREE.Mesh} explosion - 애니메이션할 폭발 메시
     */
    animateExplosion(explosion) {
        // 폭발 효과 설정
        const effect = CONFIG.EFFECTS.EXPLOSION;

        // 현재 크기 배율 (0부터 시작)
        let scale = 0;

        // 현재 프레임 수
        let frame = 0;

        // 애니메이션 함수 (재귀적으로 호출됨)
        const animate = () => {
            // 크기 증가
            scale += effect.SCALE_SPEED;

            // 프레임 카운터 증가
            frame++;

            // 폭발 크기 조정 (모든 축에 동일하게 적용)
            explosion.scale.set(scale, scale, scale);

            // 투명도 조정 (크기가 커질수록 투명해짐)
            // 1 - (scale / MAX_SCALE)
            // scale = 0 → opacity = 1 (불투명)
            // scale = MAX_SCALE → opacity = 0 (완전 투명)
            explosion.material.opacity = 1 - (scale / effect.MAX_SCALE);

            // 애니메이션 계속 조건
            // 1. 크기가 최대 크기보다 작음
            // 2. 프레임이 최대 프레임보다 작음
            if (scale < effect.MAX_SCALE && frame < effect.DURATION) {
                // 다음 프레임에 다시 호출
                // 브라우저가 최적의 타이밍에 호출 (일반적으로 60fps)
                requestAnimationFrame(animate);
            } else {
                // 애니메이션 종료: 폭발 메시 제거
                this.sceneManager.remove(explosion);
            }
        };

        // 애니메이션 시작
        animate();
    }
}
