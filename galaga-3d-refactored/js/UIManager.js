/**
 * ============================================================================
 * UI 관리자 (UIManager.js)
 * ============================================================================
 *
 * 목적: 게임 화면의 UI 요소들을 관리하고 업데이트합니다.
 *
 * 주요 책임:
 * 1. 점수, 체력, 웨이브 표시 업데이트
 * 2. 게임 시작 화면 표시/숨김
 * 3. 게임 오버 화면 표시/숨김
 * 4. 체력에 따른 색상 변경
 *
 * ============================================================================
 */

export class UIManager {
    /**
     * UI 관리자 생성자
     *
     * HTML DOM 요소들을 참조하여 저장합니다.
     */
    constructor() {
        // 게임 정보 표시 요소들
        this.scoreElement = document.getElementById('score');
        this.healthElement = document.getElementById('health');
        this.waveElement = document.getElementById('wave');

        // 화면 요소들
        this.startScreen = document.getElementById('startScreen');
        this.gameOverScreen = document.getElementById('gameOver');
        this.finalScoreElement = document.getElementById('finalScore');
    }

    /**
     * 점수 업데이트
     *
     * @param {number} score - 현재 점수
     */
    updateScore(score) {
        this.scoreElement.textContent = score;
    }

    /**
     * 체력 업데이트
     *
     * 체력값을 표시하고, 체력에 따라 색상을 변경합니다.
     * - 30 미만: 빨간색 (위험)
     * - 60 미만: 노란색 (주의)
     * - 60 이상: 녹색 (안전)
     *
     * @param {number} health - 현재 체력 (0-100)
     */
    updateHealth(health) {
        // 체력은 최소 0으로 표시
        this.healthElement.textContent = Math.max(0, health);

        // 체력에 따른 색상 변경
        if (health < 30) {
            // 위험 상태: 빨간색
            this.healthElement.style.color = '#ff0000';
        } else if (health < 60) {
            // 주의 상태: 노란색
            this.healthElement.style.color = '#ffff00';
        } else {
            // 정상 상태: 녹색
            this.healthElement.style.color = '#00ff00';
        }
    }

    /**
     * 웨이브 번호 업데이트
     *
     * @param {number} wave - 현재 웨이브 번호
     */
    updateWave(wave) {
        this.waveElement.textContent = wave;
    }

    /**
     * 시작 화면 표시
     */
    showStartScreen() {
        this.startScreen.style.display = 'block';
        this.gameOverScreen.style.display = 'none';
    }

    /**
     * 시작 화면 숨김
     */
    hideStartScreen() {
        this.startScreen.style.display = 'none';
    }

    /**
     * 게임 오버 화면 표시
     *
     * @param {number} finalScore - 최종 점수
     */
    showGameOver(finalScore) {
        this.finalScoreElement.textContent = finalScore;
        this.gameOverScreen.style.display = 'block';
    }

    /**
     * 게임 오버 화면 숨김
     */
    hideGameOver() {
        this.gameOverScreen.style.display = 'none';
    }

    /**
     * UI 초기화
     *
     * 모든 게임 정보를 초기값으로 리셋합니다.
     */
    reset() {
        this.updateScore(0);
        this.updateHealth(100);
        this.updateWave(1);
    }
}
