/**
 * ============================================================================
 * 씬 관리자 (SceneManager.js)
 * ============================================================================
 *
 * 목적:
 * Three.js의 씬(Scene), 카메라(Camera), 렌더러(Renderer)를 생성하고 관리합니다.
 * 게임의 3D 환경을 구축하는 핵심 클래스입니다.
 *
 * 주요 책임:
 * 1. Three.js 씬 초기화
 * 2. 카메라 설정 및 위치 조정
 * 3. 렌더러 생성 (WebGL)
 * 4. 조명 시스템 구축
 * 5. 배경 별 필드 생성
 * 6. 화면 크기 변경 대응 (반응형)
 *
 * 사용 예:
 * const sceneManager = new SceneManager();
 * sceneManager.add(myObject);  // 씬에 객체 추가
 * sceneManager.render();        // 화면 렌더링
 * ============================================================================
 */

import { CONFIG } from './config.js';

export class SceneManager {
    /**
     * SceneManager 생성자
     *
     * 자동으로 모든 Three.js 환경을 초기화합니다:
     * - 씬, 카메라, 렌더러
     * - 조명 시스템
     * - 별 배경
     * - 윈도우 리사이즈 이벤트 리스너
     */
    constructor() {
        // Three.js 핵심 객체들을 저장할 속성
        this.scene = null;       // 3D 씬 (모든 3D 객체를 담는 컨테이너)
        this.camera = null;      // 카메라 (보는 시점)
        this.renderer = null;    // 렌더러 (화면에 그리는 역할)
        this.starField = null;   // 별 배경 객체

        // 초기화 메서드 호출
        this.init();
    }

    /**
     * 초기화 메서드
     *
     * Three.js 환경을 구축하는 모든 단계를 순서대로 실행합니다.
     * 각 단계는 독립적인 메서드로 분리되어 있어 유지보수가 쉽습니다.
     */
    init() {
        this.createScene();      // 1. 씬 생성
        this.createCamera();     // 2. 카메라 설정
        this.createRenderer();   // 3. 렌더러 설정
        this.createLighting();   // 4. 조명 추가
        this.createStarField();  // 5. 별 배경 생성

        // 윈도우 크기가 변경될 때 자동으로 대응
        window.addEventListener('resize', () => this.onWindowResize());
    }

    /**
     * 씬(Scene) 생성
     *
     * Three.js의 씬은 모든 3D 객체를 담는 컨테이너입니다.
     * 플레이어, 적, 총알 등 모든 게임 객체가 씬에 추가됩니다.
     */
    createScene() {
        // 새로운 씬 객체 생성
        this.scene = new THREE.Scene();

        // 안개(Fog) 효과 추가
        // 멀리 있는 객체를 점점 흐리게 만들어 깊이감을 연출
        this.scene.fog = new THREE.Fog(
            CONFIG.SCENE.FOG_COLOR,  // 안개 색상 (검은색)
            CONFIG.SCENE.FOG_NEAR,   // 안개 시작 거리
            CONFIG.SCENE.FOG_FAR     // 안개 최대 거리
        );
    }

    /**
     * 카메라(Camera) 생성 및 설정
     *
     * PerspectiveCamera: 원근감이 있는 카메라 (인간의 눈과 유사)
     * 가까운 것은 크게, 먼 것은 작게 보입니다.
     */
    createCamera() {
        // 원근 투영 카메라 생성
        this.camera = new THREE.PerspectiveCamera(
            CONFIG.CAMERA.FOV,                          // 시야각 (Field of View)
            window.innerWidth / window.innerHeight,     // 화면 비율 (가로/세로)
            CONFIG.CAMERA.NEAR,                         // 최소 렌더링 거리
            CONFIG.CAMERA.FAR                           // 최대 렌더링 거리
        );

        // 카메라 위치 설정 (x, y, z)
        const pos = CONFIG.CAMERA.POSITION;
        this.camera.position.set(pos.x, pos.y, pos.z);

        // 카메라가 바라보는 지점 설정 (중앙을 향하도록)
        const lookAt = CONFIG.CAMERA.LOOK_AT;
        this.camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
    }

    /**
     * 렌더러(Renderer) 생성 및 설정
     *
     * WebGLRenderer: GPU를 사용하여 3D 씬을 2D 화면에 그립니다.
     * 캔버스 요소에 연결되어 실제 그래픽을 표시합니다.
     */
    createRenderer() {
        // HTML에서 캔버스 요소 찾기
        const canvas = document.getElementById('gameCanvas');

        // WebGL 렌더러 생성
        this.renderer = new THREE.WebGLRenderer({
            canvas,              // 렌더링할 캔버스 요소
            antialias: true      // 안티앨리어싱 (계단 현상 제거)
        });

        // 렌더러 크기를 브라우저 윈도우 크기에 맞춤
        this.renderer.setSize(window.innerWidth, window.innerHeight);

        // 그림자 효과 활성화 (성능에 영향 있음)
        this.renderer.shadowMap.enabled = true;
    }

    /**
     * 조명(Lighting) 시스템 생성
     *
     * 3D 객체를 보기 위해서는 빛이 필요합니다.
     * 다양한 조명을 조합하여 극적인 분위기를 연출합니다.
     *
     * 조명 종류:
     * 1. Ambient Light: 전체적인 밝기 (그림자 없음)
     * 2. Directional Light: 태양광 같은 평행광 (그림자 있음)
     * 3. Point Light: 전구처럼 모든 방향으로 퍼지는 빛
     */
    createLighting() {
        // 1. 주변광 (Ambient Light)
        // 모든 객체를 균일하게 비춥니다 (그림자 없음)
        const ambientLight = new THREE.AmbientLight(
            CONFIG.LIGHTS.AMBIENT.COLOR,       // 조명 색상
            CONFIG.LIGHTS.AMBIENT.INTENSITY    // 밝기
        );
        this.scene.add(ambientLight);

        // 2. 방향성 조명 (Directional Light)
        // 태양광처럼 한 방향에서 비추는 조명 (그림자 있음)
        const directionalLight = new THREE.DirectionalLight(
            CONFIG.LIGHTS.DIRECTIONAL.COLOR,      // 조명 색상
            CONFIG.LIGHTS.DIRECTIONAL.INTENSITY   // 밝기
        );

        // 조명의 위치 설정
        const dirPos = CONFIG.LIGHTS.DIRECTIONAL.POSITION;
        directionalLight.position.set(dirPos.x, dirPos.y, dirPos.z);

        // 그림자 생성 활성화
        directionalLight.castShadow = true;

        this.scene.add(directionalLight);

        // 3. 점광원들 (Point Lights)
        // 특정 위치에서 모든 방향으로 빛을 발산 (전구와 유사)
        // 녹색과 분홍색 조명으로 사이버펑크 분위기 연출
        CONFIG.LIGHTS.POINT_LIGHTS.forEach(lightConfig => {
            const pointLight = new THREE.PointLight(
                lightConfig.color,        // 조명 색상
                lightConfig.intensity,    // 밝기
                lightConfig.distance      // 빛이 닿는 거리
            );

            // 조명 위치 설정
            const pos = lightConfig.position;
            pointLight.position.set(pos.x, pos.y, pos.z);

            this.scene.add(pointLight);
        });
    }

    /**
     * 별 필드(Star Field) 생성
     *
     * 우주 배경을 표현하기 위한 별들을 생성합니다.
     * 무작위 위치에 다양한 색상의 별을 배치하여
     * 화려한 우주 배경을 만듭니다.
     *
     * 기술:
     * - BufferGeometry: 효율적인 점 렌더링
     * - PointsMaterial: 점 스타일 재질
     * - Vertex Colors: 각 별마다 다른 색상
     */
    createStarField() {
        // 기하학 객체 생성 (정점 데이터를 담을 컨테이너)
        const geometry = new THREE.BufferGeometry();
        const vertices = [];  // 별의 위치 (x, y, z) 배열
        const colors = [];    // 별의 색상 (r, g, b) 배열
        const range = CONFIG.STARS.RANGE;

        // 설정된 개수만큼 별 생성
        for (let i = 0; i < CONFIG.STARS.COUNT; i++) {
            // 무작위 위치 생성 (3D 공간에 고르게 분포)
            vertices.push(
                Math.random() * range - range / 2,  // x: -100 ~ 100
                Math.random() * range - range / 2,  // y: -100 ~ 100
                Math.random() * range - range / 2   // z: -100 ~ 100
            );

            // 무작위 색상 생성 (HSL 색 공간 사용)
            const color = new THREE.Color();
            color.setHSL(
                Math.random(),  // Hue: 색조 (0~1, 무지개 색상)
                0.5,           // Saturation: 채도 (중간)
                0.5            // Lightness: 밝기 (중간)
            );
            colors.push(color.r, color.g, color.b);
        }

        // 위치 데이터를 기하학에 설정
        // Float32Array: GPU에 효율적으로 전달하기 위한 배열 타입
        // 3: 각 정점이 x, y, z 세 개의 값을 가짐
        geometry.setAttribute('position',
            new THREE.Float32BufferAttribute(vertices, 3)
        );

        // 색상 데이터를 기하학에 설정
        geometry.setAttribute('color',
            new THREE.Float32BufferAttribute(colors, 3)
        );

        // 점 재질 생성 (별을 점으로 렌더링)
        const material = new THREE.PointsMaterial({
            size: CONFIG.STARS.SIZE,     // 점의 크기
            vertexColors: true,          // 각 정점의 색상 사용
            transparent: true,           // 투명도 사용
            opacity: 0.8                 // 약간 투명하게
        });

        // Points 객체 생성 (기하학 + 재질)
        this.starField = new THREE.Points(geometry, material);

        // 씬에 추가
        this.scene.add(this.starField);
    }

    /**
     * 업데이트 메서드
     *
     * 매 프레임마다 호출되어 씬을 업데이트합니다.
     * 현재는 별 배경을 천천히 회전시킵니다.
     */
    update() {
        // 별 배경이 존재하면 회전
        if (this.starField) {
            // y축 회전 (좌우)
            this.starField.rotation.y += CONFIG.STARS.ROTATION_SPEED.y;

            // z축 회전 (기울기)
            this.starField.rotation.z += CONFIG.STARS.ROTATION_SPEED.z;
        }
    }

    /**
     * 렌더링 메서드
     *
     * 현재 씬을 카메라 시점에서 렌더링합니다.
     * 매 프레임마다 호출되어 화면을 갱신합니다.
     */
    render() {
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * 윈도우 크기 변경 이벤트 핸들러
     *
     * 브라우저 크기가 변경될 때 호출됩니다.
     * 카메라와 렌더러를 새로운 크기에 맞춥니다.
     *
     * 반응형 디자인의 핵심 메서드입니다.
     */
    onWindowResize() {
        // 카메라의 화면 비율 업데이트
        this.camera.aspect = window.innerWidth / window.innerHeight;

        // 카메라 투영 행렬 재계산
        // aspect를 변경한 후 반드시 호출해야 함
        this.camera.updateProjectionMatrix();

        // 렌더러 크기 업데이트
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    /**
     * 씬에 객체 추가
     *
     * @param {THREE.Object3D} object - 추가할 3D 객체
     */
    add(object) {
        this.scene.add(object);
    }

    /**
     * 씬에서 객체 제거
     *
     * @param {THREE.Object3D} object - 제거할 3D 객체
     */
    remove(object) {
        this.scene.remove(object);
    }

    /**
     * 씬 객체 반환 (Getter)
     *
     * @returns {THREE.Scene} Three.js 씬 객체
     */
    getScene() {
        return this.scene;
    }

    /**
     * 카메라 객체 반환 (Getter)
     *
     * @returns {THREE.PerspectiveCamera} Three.js 카메라 객체
     */
    getCamera() {
        return this.camera;
    }
}
