import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { Bearing6205 } from "./parts/Bearing6205";
import { PartPicker } from "./controls/PartPicker";
import { createMetalMaterial, createDarkMetalMaterial, createAccentMaterial, FAULT_COLORS } from "./materials/IndustrialMaterials";
export class SceneManager {
    scene;
    camera;
    renderer;
    controls;
    picker;
    bearing;
    frame = 0;
    startTime = performance.now();
    faultKey = "normal";
    twinTarget = "";
    disposed = false;
    // Parts registry for interaction
    parts = [];
    constructor(opts) {
        const { container } = opts;
        const W = container.clientWidth || 800;
        const H = container.clientHeight || 600;
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x081422);
        this.scene.fog = new THREE.FogExp2(0x081422, 0.035);
        // Camera
        this.camera = new THREE.PerspectiveCamera(38, W / H, 0.1, 100);
        this.camera.position.set(8, 5, 8);
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
        this.renderer.setSize(W, H);
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;
        container.appendChild(this.renderer.domElement);
        // Controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.08;
        this.controls.target.set(0, 0.6, 0);
        this.controls.maxPolarAngle = Math.PI * 0.78;
        this.controls.minDistance = 2;
        this.controls.maxDistance = 18;
        // Picker
        this.picker = new PartPicker(container, this.camera);
        this.picker.onHover = (name) => opts.onPartHover?.(name);
        this.picker.onClick = (name) => opts.onPartClick?.(name);
        // Lighting
        this.setupLighting();
        // Build scene
        this.bearing = this.buildExperimentPlatform();
        // Grid
        const grid = new THREE.GridHelper(24, 36, 0x245c7a, 0x123044);
        grid.position.y = -0.39;
        this.scene.add(grid);
        // Register parts with picker
        this.picker.register(...this.parts);
        // Resize
        const ro = new ResizeObserver(() => this.resize());
        ro.observe(container);
        container._sceneObserver = ro;
        // Start loop
        this.animate();
    }
    setupLighting() {
        this.scene.add(new THREE.HemisphereLight(0x9edfff, 0x06101b, 2.8));
        const key = new THREE.DirectionalLight(0xffffff, 4);
        key.position.set(4, 8, 6);
        this.scene.add(key);
        const fill = new THREE.DirectionalLight(0x8fcfff, 1.5);
        fill.position.set(-3, 4, -4);
        this.scene.add(fill);
        const rim = new THREE.DirectionalLight(0x4f8fff, 0.8);
        rim.position.set(-2, 1, -5);
        this.scene.add(rim);
    }
    buildExperimentPlatform() {
        const metal = createMetalMaterial();
        const dark = createDarkMetalMaterial();
        const accent = createAccentMaterial();
        // === Base Platform ===
        const base = new THREE.Mesh(new THREE.BoxGeometry(10, 0.35, 2.7), metal);
        base.position.y = -0.2;
        base.userData.partName = "base_platform";
        this.scene.add(base);
        this.parts.push(base);
        // Rails / T-slots
        for (const x of [-4.6, -2.8, -1.1, 0.9, 2.7, 4.4]) {
            const rail = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 2.9), dark);
            rail.position.set(x, 0.02, 0);
            this.scene.add(rail);
        }
        // Bolt holes
        for (const [bx, bz] of [[-4.8, -1.2], [-4.8, 1.2], [4.8, -1.2], [4.8, 1.2]]) {
            const hole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.1, 12), new THREE.MeshStandardMaterial({ color: 0x0a1420 }));
            hole.position.set(bx, -0.05, bz);
            this.scene.add(hole);
        }
        // === Motor ===
        const motor = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 1.05, 2.2, 32), dark);
        motor.rotation.z = Math.PI / 2;
        motor.position.set(-3.7, 0.85, 0);
        motor.userData.partName = "motor";
        this.scene.add(motor);
        this.parts.push(motor);
        // Cooling fins
        for (let i = 0; i < 10; i++) {
            const fin = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.72, 2.34), new THREE.MeshStandardMaterial({ color: 0x0f1d27, metalness: 0.45, roughness: 0.55 }));
            fin.position.set(-4.42 + i * 0.14, 0.85, 0);
            this.scene.add(fin);
        }
        // Terminal box
        const termBox = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.28, 0.45), dark);
        termBox.position.set(-3.7, 1.58, -1.15);
        this.scene.add(termBox);
        // Speed controller
        const ctrl = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.7, 0.5), new THREE.MeshStandardMaterial({ color: 0x10283a, emissive: 0x0b4d62, emissiveIntensity: 0.18, metalness: 0.3, roughness: 0.45 }));
        ctrl.position.set(-2.55, 1.35, -0.78);
        ctrl.userData.partName = "speed_controller";
        this.scene.add(ctrl);
        this.parts.push(ctrl);
        // Coupling
        const cp = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.52, 32), new THREE.MeshStandardMaterial({ color: 0xdfe8ea, emissive: 0x1c3b48, emissiveIntensity: 0.08, metalness: 0.65, roughness: 0.18 }));
        cp.rotation.z = Math.PI / 2;
        cp.position.set(-2.15, 0.8, 0);
        cp.userData.partName = "coupling";
        this.scene.add(cp);
        this.parts.push(cp);
        // Shaft
        const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 7.2, 24), metal);
        shaft.rotation.z = Math.PI / 2;
        shaft.position.set(0.3, 0.8, 0);
        shaft.userData.partName = "shaft";
        this.scene.add(shaft);
        this.parts.push(shaft);
        // Guard
        const guard = new THREE.Mesh(new THREE.BoxGeometry(2.25, 1.35, 1.55), new THREE.MeshPhysicalMaterial({ color: 0x8fdfff, transparent: true, opacity: 0.16, roughness: 0.12, metalness: 0, transmission: 0.2 }));
        guard.position.set(0.15, 0.95, 0);
        this.scene.add(guard);
        // === Bearing 6205 ===
        const bearing = new Bearing6205();
        bearing.group.position.set(-0.3, 0.8, 0);
        this.scene.add(bearing.group);
        this.parts.push(bearing.group);
        // Bearing support
        const bSupp = new THREE.Mesh(new THREE.BoxGeometry(0.38, 1.45, 1.35), dark);
        bSupp.position.set(-0.3, 0.35, 0);
        bSupp.userData.partName = "bearing_support";
        this.scene.add(bSupp);
        this.parts.push(bSupp);
        // Right support
        const rSupp = new THREE.Mesh(new THREE.BoxGeometry(0.38, 1.45, 1.35), dark);
        rSupp.position.set(1.8, 0.35, 0);
        rSupp.userData.partName = "support_right";
        this.scene.add(rSupp);
        this.parts.push(rSupp);
        // Pulse light at bearing
        const pulse = new THREE.PointLight(FAULT_COLORS.normal.color, 0, 2.5);
        pulse.position.set(-0.3, 1.1, 0.72);
        pulse.name = "bearing_pulse";
        this.scene.add(pulse);
        // === Sensors (3-axis) ===
        const sensorConfigs = [
            { x: -0.72, z: -0.74, color: 0x35c8ff, label: "X" },
            { x: 0.18, z: 0.72, color: 0x35e0a0, label: "Y" },
            { x: 1.55, z: -0.66, color: 0xffc34c, label: "Z" },
        ];
        for (const cfg of sensorConfigs) {
            const body = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.18), new THREE.MeshStandardMaterial({ color: 0xc7d1d5, emissive: cfg.color, emissiveIntensity: 0.28, metalness: 0.55, roughness: 0.25 }));
            body.position.set(cfg.x, 1.15, cfg.z);
            body.userData.partName = "sensor_" + cfg.label.toLowerCase();
            this.scene.add(body);
            this.parts.push(body);
            const cable = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.9, 8), new THREE.MeshBasicMaterial({ color: cfg.color }));
            cable.rotation.x = Math.PI / 2;
            cable.position.set(cfg.x, 0.82, cfg.z * 0.75);
            this.scene.add(cable);
        }
        // === Gearbox ===
        const gb = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.78, 1.05, 36), new THREE.MeshStandardMaterial({ color: 0x80906f, metalness: 0.55, roughness: 0.34 }));
        gb.rotation.z = Math.PI / 2;
        gb.position.set(2.2, 0.8, 0);
        gb.userData.partName = "gearbox";
        this.scene.add(gb);
        this.parts.push(gb);
        // Planet gears
        const pg = new THREE.Group();
        pg.position.set(2.2, 0.8, 0);
        for (let i = 0; i < 3; i++) {
            const planet = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.12, 18), metal);
            planet.rotation.z = Math.PI / 2;
            planet.position.set(0, Math.sin(i * 2.09) * 0.42, Math.cos(i * 2.09) * 0.42);
            pg.add(planet);
        }
        this.scene.add(pg);
        // Load disk
        const disk = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.45, 36), metal);
        disk.rotation.z = Math.PI / 2;
        disk.position.set(3.5, 0.8, 0);
        disk.userData.partName = "load_disk";
        this.scene.add(disk);
        this.parts.push(disk);
        // Brake glow
        const bg = new THREE.Mesh(new THREE.TorusGeometry(1.24, 0.035, 10, 48), new THREE.MeshBasicMaterial({ color: 0xffc15a }));
        bg.rotation.y = Math.PI / 2;
        bg.position.set(3.72, 0.8, 0);
        this.scene.add(bg);
        return bearing;
    }
    /** Update fault state for all parts */
    setFault(faultKey, twinTarget) {
        this.faultKey = faultKey;
        this.twinTarget = twinTarget || "";
        this.bearing.setFault({ type: faultKey, intensity: 0.5, target: this.getFaultTarget() });
    }
    getFaultTarget() {
        const t = this.twinTarget;
        if (t.includes("inner"))
            return "inner";
        if (t.includes("outer"))
            return "outer";
        if (t.includes("rolling"))
            return "rolling";
        if (t.includes("compound"))
            return "compound";
        return undefined;
    }
    /** Resize handler */
    resize() {
        const el = this.renderer.domElement.parentElement;
        if (!el)
            return;
        const W = el.clientWidth;
        const H = el.clientHeight;
        this.camera.aspect = W / H;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(W, H);
    }
    /** Main animation loop */
    animate = () => {
        if (this.disposed)
            return;
        this.frame = requestAnimationFrame(this.animate);
        const dt = 0.016;
        const t = performance.now() * 0.006;
        // Update bearing
        this.bearing.update(dt);
        // Rotating parts
        const shaft = this.parts.find(p => p.userData.partName === "shaft");
        if (shaft)
            shaft.rotation.x += 0.02;
        const motor = this.parts.find(p => p.userData.partName === "motor");
        if (motor)
            motor.rotation.x += 0.01;
        const coupling = this.parts.find(p => p.userData.partName === "coupling");
        if (coupling)
            coupling.rotation.x += 0.04;
        const gearbox = this.parts.find(p => p.userData.partName === "gearbox");
        if (gearbox)
            gearbox.rotation.x += 0.018;
        const disk = this.parts.find(p => p.userData.partName === "load_disk");
        if (disk)
            disk.rotation.x += 0.025;
        // Pulse light
        const pulse = this.scene.getObjectByName("bearing_pulse");
        if (pulse) {
            const isNormal = this.faultKey === "normal";
            pulse.intensity = isNormal ? 0.25 : 1.8 + Math.sin(t * 4) * 1.2;
            const color = FAULT_COLORS[this.faultKey] || FAULT_COLORS.unknown;
            pulse.color.setHex(color.color);
        }
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    };
    /** Stop animation and clean up */
    dispose() {
        this.disposed = true;
        cancelAnimationFrame(this.frame);
        this.picker.dispose();
        this.controls.dispose();
        this.renderer.dispose();
        const el = this.renderer.domElement;
        if (el.parentElement) {
            el.parentElement.removeChild(el);
            delete el.parentElement._sceneObserver;
        }
    }
}
