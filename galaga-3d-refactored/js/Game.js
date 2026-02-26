/**
 * ============================================================================
 * 게임 메인 클래스 (Game.js)
 * ============================================================================
 *
 * 목적: 게임의 모든 시스템을 조율하는 메인 컨트롤러입니다.
 *
 * 주요 책임:
 * 1. 모든 매니저 초기화 및 생명주기 관리
 * 2. 게임 루프 실행 (업데이트 → 렌더링)
 * 3. 게임 상태 관리 (시작, 플레이 중, 게임 오버)
 * 4. 이벤트 조율 (발사, 충돌, 점수, 피해)
 * 5. 웨이브 시스템 관리
 *
 * 디자인 패턴:
 * - 중재자 패턴 (Mediator Pattern): 모든 매니저를 조율
 * - 게임 루프 패턴: requestAnimationFrame 기반
 * - 의존성 주입: 매니저들에게 sceneManager 주입
 *
 * 아키텍처:
 * Game는 모든 매니저의 인스턴스를 가지고 있으며,
 * 각 매니저는 Game을 통해 간접적으로 통신합니다.
 *
 * ============================================================================
 */

import { CONFIG } from './config.js';
import { SceneManager } from './SceneManager.js';
import { Player } from './Player.js';
import { EnemyManager } from './EnemyManager.js';
import { BulletManager } from './BulletManager.js';
import { CollisionManager } from './CollisionManager.js';
import { UIManager } from './UIManager.js';

export class Game {
    /**
     * 게임 생성자
     *
     * 모든 매니저를 초기화하고 이벤트 리스너를 설정합니다.
     * 게임은 'start' 상태로 시작하며, 사용자가 시작 버튼을 누를 때까지 대기합니다.
     */
    constructor() {
        // 게임 상태: 'start'(시작 전), 'playing'(플레이 중), 'gameOver'(게임 오버)
        this.state = 'start';

        // 현재 점수
        this.score = 0;

        // requestAnimationFrame이 반환하는 애니메이션 ID
        // 게임 루프를 중지할 때 사용
        this.animationId = null;

        // === 매니저 초기화 ===

        // Three.js 씬 관리자 (씬, 카메라, 렌더러, 조명, 별 배경)
        this.sceneManager = new SceneManager();

        // UI 관리자 (점수, 체력, 웨이브 표시)
        this.uiManager = new UIManager();

        // 총알 관리자 (플레이어/적 총알 생성 및 관리)
        this.bulletManager = new BulletManager(this.sceneManager);

        // 적 관리자 (적 생성, 웨이브 시스템)
        this.enemyManager = new EnemyManager(this.sceneManager);

        // 충돌 관리자 (충돌 감지 및 폭발 효과)
        this.collisionManager = new CollisionManager(this.sceneManager);

        // 플레이어 객체 (게임 시작 시 생성됨)
        this.player = null;

        // 웨이브 스폰 타이머 ID
        // 웨이브 간 딜레이를 위해 사용
        this.waveSpawnTimer = null;

        // 이벤트 리스너 설정
        this.setupEventListeners();
    }

    /**
     * 이벤트 리스너 설정
     *
     * 마우스 클릭 이벤트와 HTML 버튼 이벤트를 연결합니다.
     */
    setupEventListeners() {
        // 마우스 클릭으로 발사
        document.addEventListener('click', () => {
            // 게임 플레이 중이고 플레이어가 존재할 때만
            if (this.state === 'playing' && this.player) {
                this.handlePlayerShoot();
            }
        });

        // HTML 버튼에서 호출할 수 있도록 window 객체에 메서드 노출
        // index.html에서 onclick="startGame()"로 호출됨
        window.startGame = () => this.start();
        window.restartGame = () => this.restart();
    }

    /**
     * 게임 시작 메서드
     *
     * 새 게임을 시작합니다. 플레이어와 첫 웨이브를 생성하고
     * 게임 루프를 시작합니다.
     */
    start() {
        // 게임 상태를 '플레이 중'으로 변경
        this.state = 'playing';

        // 점수 초기화
        this.score = 0;

        // 시작 화면과 게임 오버 화면 숨김
        this.uiManager.hideStartScreen();
        this.uiManager.hideGameOver();

        // UI 초기화 (점수 0, 체력 100, 웨이브 1)
        this.uiManager.reset();

        // 플레이어 생성
        this.player = new Player(this.sceneManager);

        // 첫 번째 웨이브 생성
        this.enemyManager.spawnWave();

        // 게임 루프 시작
        this.gameLoop();
    }

    /**
     * 게임 재시작 메서드
     *
     * 현재 게임을 정리하고 새 게임을 시작합니다.
     * 게임 오버 후 "PLAY AGAIN" 버튼을 누를 때 호출됩니다.
     */
    restart() {
        // 현재 게임 정리 (플레이어, 적, 총알 제거)
        this.cleanup();

        // 매니저 리셋 (적과 총알 배열 비우기)
        this.enemyManager.reset();
        this.bulletManager.reset();

        // 새 게임 시작
        this.start();
    }

    /**
     * 게임 정리 메서드
     *
     * 게임 재시작이나 종료 시 모든 게임 객체를 정리합니다.
     * 메모리 누수를 방지하기 위해 타이머와 애니메이션도 중지합니다.
     */
    cleanup() {
        // 게임 루프 중지
        if (this.animationId) {
            // requestAnimationFrame 취소
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        // 웨이브 스폰 타이머 정리
        if (this.waveSpawnTimer) {
            // setTimeout 취소
            clearTimeout(this.waveSpawnTimer);
            this.waveSpawnTimer = null;
        }

        // 플레이어 파괴
        if (this.player) {
            // 씬에서 플레이어 제거
            this.player.destroy();
            this.player = null;
        }
    }

    /**
     * 게임 루프 메서드
     *
     * 매 프레임마다 호출되는 메인 게임 루프입니다.
     * 게임이 '플레이 중' 상태일 때만 실행됩니다.
     *
     * 게임 루프 구조:
     * 1. requestAnimationFrame으로 다음 프레임 예약
     * 2. 게임 상태 업데이트 (로직)
     * 3. 화면 렌더링 (그래픽)
     *
     * 일반적으로 60fps(1초에 60번) 실행됩니다.
     */
    gameLoop() {
        // 게임이 플레이 중이 아니면 루프 중지
        if (this.state !== 'playing') return;

        // 다음 프레임에 gameLoop 재호출 예약
        // requestAnimationFrame은 브라우저가 최적의 시간에 호출
        // 반환값(ID)을 저장하여 나중에 취소할 수 있음
        this.animationId = requestAnimationFrame(() => this.gameLoop());

        // 게임 로직 업데이트
        this.update();

        // 화면 렌더링
        this.render();
    }

    /**
     * 게임 업데이트 메서드
     *
     * 모든 게임 객체의 상태를 업데이트하고 이벤트를 처리합니다.
     * 이 메서드는 게임의 핵심 로직이 실행되는 곳입니다.
     *
     * 업데이트 순서:
     * 1. 플레이어 업데이트 (이동, 발사)
     * 2. 씬 업데이트 (별 배경 회전)
     * 3. 적 업데이트 (이동, 발사 판정)
     * 4. 총알 업데이트 (이동, 제거)
     * 5. 충돌 감지 (총알 vs 적, 총알 vs 플레이어)
     * 6. 결과 처리 (점수, 피해, 폭발)
     * 7. 웨이브 완료 체크
     */
    update() {
        // 1. 플레이어 업데이트
        if (this.player) {
            // 플레이어 이동 및 회전
            this.player.update();

            // 스페이스바가 눌려있는지 확인하여 발사
            if (this.player.isShootKeyPressed()) {
                this.handlePlayerShoot();
            }
        }

        // 2. 씬 업데이트 (별 배경 회전)
        this.sceneManager.update();

        // 3. 적 업데이트
        const enemyResults = this.enemyManager.update();

        // 플레이어를 통과한 적 처리
        if (enemyResults.escaped.length > 0) {
            // 각 탈출한 적에 대해 플레이어 피해 처리
            enemyResults.escaped.forEach(result => {
                this.handlePlayerDamage(result.damage);
            });
        }

        // 발사해야 하는 적들의 총알 생성
        enemyResults.shouldShoot.forEach(position => {
            this.bulletManager.shootEnemyBullet(position);
        });

        // 4. 총알 업데이트 (이동 및 화면 밖 제거)
        this.bulletManager.update();

        // 5. 충돌 감지
        const collisionResults = this.collisionManager.checkCollisions(
            this.player,           // 플레이어 객체
            this.enemyManager,     // 적 관리자
            this.bulletManager     // 총알 관리자
        );

        // 6. 충돌 결과 처리

        // 점수 획득
        if (collisionResults.score > 0) {
            this.addScore(collisionResults.score);
        }

        // 플레이어 피해
        if (collisionResults.playerDamage > 0) {
            this.handlePlayerDamage(collisionResults.playerDamage);
        }

        // 폭발 효과 생성
        if (collisionResults.explosions.length > 0) {
            collisionResults.explosions.forEach(position => {
                this.collisionManager.createExplosion(position);
            });
        }

        // 7. 웨이브 완료 체크
        // 적이 모두 제거되고, 웨이브 스폰 타이머가 없으면
        if (this.enemyManager.isEmpty() && !this.waveSpawnTimer) {
            // 다음 웨이브로 진행
            this.nextWave();
        }
    }

    /**
     * 렌더링 메서드
     *
     * 씬 관리자를 통해 화면을 렌더링합니다.
     * Three.js가 현재 씬을 카메라 시점에서 그립니다.
     */
    render() {
        this.sceneManager.render();
    }

    /**
     * 플레이어 발사 처리 메서드
     *
     * 플레이어가 총알을 발사할 수 있는지 확인하고,
     * 가능하면 플레이어 위치에서 총알을 생성합니다.
     */
    handlePlayerShoot() {
        // 플레이어가 존재하고 발사 가능하면 (쿨다운 체크)
        if (this.player && this.player.canShoot()) {
            // 플레이어 위치에서 총알 발사
            this.bulletManager.shootPlayerBullet(this.player.getPosition());
        }
    }

    /**
     * 플레이어 피해 처리 메서드
     *
     * 플레이어가 피해를 입었을 때 호출됩니다.
     * 체력을 감소시키고 UI를 업데이트하며,
     * 체력이 0 이하면 게임 오버 처리를 합니다.
     *
     * @param {number} damage - 받는 피해량
     */
    handlePlayerDamage(damage) {
        // 플레이어가 존재하지 않으면 아무것도 하지 않음
        if (!this.player) return;

        // 플레이어에게 피해 입힘
        // 새로운 체력 반환 (음수가 될 수 있음)
        const newHealth = this.player.takeDamage(damage);

        // UI 업데이트 (체력 표시 및 색상 변경)
        this.uiManager.updateHealth(newHealth);

        // 체력이 0 이하면 게임 오버
        if (newHealth <= 0) {
            this.gameOver();
        }
    }

    /**
     * 점수 추가 메서드
     *
     * 점수를 추가하고 UI를 업데이트합니다.
     *
     * @param {number} points - 추가할 점수
     */
    addScore(points) {
        // 점수 증가
        this.score += points;

        // UI 업데이트
        this.uiManager.updateScore(this.score);
    }

    /**
     * 다음 웨이브로 진행 메서드
     *
     * 현재 웨이브의 모든 적을 처치했을 때 호출됩니다.
     * 웨이브 번호를 증가시키고, 일정 시간 후 새 웨이브를 생성합니다.
     */
    nextWave() {
        // 웨이브 번호 증가 및 적 수 증가
        this.enemyManager.nextWave();

        // UI에 새 웨이브 번호 표시
        this.uiManager.updateWave(this.enemyManager.getCurrentWave());

        // 일정 시간 후 새 웨이브 생성
        // 플레이어에게 준비 시간 제공
        this.waveSpawnTimer = setTimeout(() => {
            // 새 웨이브 생성
            this.enemyManager.spawnWave();

            // 타이머 참조 제거
            this.waveSpawnTimer = null;
        }, CONFIG.WAVE.SPAWN_DELAY);
    }

    /**
     * 게임 오버 메서드
     *
     * 플레이어 체력이 0이 되었을 때 호출됩니다.
     * 게임 상태를 변경하고 게임 오버 화면을 표시합니다.
     */
    gameOver() {
        // 게임 상태를 '게임 오버'로 변경
        // 이렇게 하면 게임 루프가 자동으로 중지됨
        this.state = 'gameOver';

        // 게임 오버 화면 표시 (최종 점수 포함)
        this.uiManager.showGameOver(this.score);
    }

    /**
     * 게임 상태 반환 (Getter)
     *
     * @returns {string} 현재 게임 상태 ('start', 'playing', 'gameOver')
     */
    getState() {
        return this.state;
    }
}
