import * as THREE from "three";
import { createPolishedMaterial, createMetalMaterial, applyFaultMaterial } from "../materials/IndustrialMaterials";
export class Bearing6205 {
    group = new THREE.Group();
    outerRace;
    innerRace;
    balls = [];
    cage;
    defectSpot;
    ballOrbitGroup = new THREE.Group();
    time = 0;
    faultState = { type: "normal", intensity: 0 };
    constructor() {
        // --- Outer Race ---
        this.outerRace = new THREE.Mesh(new THREE.TorusGeometry(0.78, 0.08, 24, 64), createMetalMaterial({ color: 0x3f5364, emissive: 0x3f5364, emissiveIntensity: 0.03 }));
        this.outerRace.rotation.y = Math.PI / 2;
        this.outerRace.userData.partName = "bearing_outer_race";
        this.group.add(this.outerRace);
        // --- Inner Race ---
        this.innerRace = new THREE.Mesh(new THREE.TorusGeometry(0.38, 0.08, 24, 64), createPolishedMaterial({ color: 0x546879, emissive: 0x546879, emissiveIntensity: 0.03 }));
        this.innerRace.rotation.y = Math.PI / 2;
        this.innerRace.userData.partName = "bearing_inner_race";
        this.group.add(this.innerRace);
        // --- 9 Balls (6205 standard) ---
        const ballMat = new THREE.MeshStandardMaterial({
            color: 0x9aa7b4,
            metalness: 0.6,
            roughness: 0.28,
            emissive: 0x22384a,
            emissiveIntensity: 0.05,
        });
        for (let i = 0; i < 9; i++) {
            const angle = (i / 9) * Math.PI * 2;
            const ball = new THREE.Mesh(new THREE.SphereGeometry(0.095, 20, 16), ballMat.clone());
            ball.position.set(Math.sin(angle) * 0.56, 0, Math.cos(angle) * 0.56);
            ball.userData.ballIndex = i;
            ball.userData.partName = `ball_${i + 1}`;
            this.balls.push(ball);
            this.ballOrbitGroup.add(ball);
        }
        this.group.add(this.ballOrbitGroup);
        // --- Cage (transparent) ---
        this.cage = new THREE.Mesh(new THREE.TorusGeometry(0.56, 0.025, 12, 48), new THREE.MeshPhysicalMaterial({
            color: 0x7a8894,
            metalness: 0.5,
            roughness: 0.4,
            transparent: true,
            opacity: 0.4,
        }));
        this.cage.rotation.y = Math.PI / 2;
        this.cage.userData.partName = "bearing_cage";
        this.group.add(this.cage);
        // --- Defect Spot (visible in fault conditions) ---
        this.defectSpot = new THREE.Mesh(new THREE.SphereGeometry(0.08, 18, 12), new THREE.MeshStandardMaterial({
            color: 0xff4868,
            emissive: 0xff4868,
            emissiveIntensity: 0,
            metalness: 0.2,
            roughness: 0.2,
        }));
        this.defectSpot.position.set(0, 0.39, 0.34);
        this.defectSpot.visible = false;
        this.defectSpot.userData.partName = "defect_spot";
        this.group.add(this.defectSpot);
        // Wrap in a container for raycasting
        this.group.userData.partName = "bearing_6205";
    }
    /** Set fault state and update visual appearance */
    setFault(state) {
        this.faultState = state;
        this.defectSpot.visible = state.type !== "normal";
        // Reset all materials
        this.balls.forEach((b) => {
            const m = b.material;
            m.color.setHex(0x9aa7b4);
            m.emissive.setHex(0x22384a);
            m.emissiveIntensity = 0.05;
        });
        switch (state.type) {
            case "normal":
                applyFaultMaterial(this.innerRace, "normal", 0.12);
                applyFaultMaterial(this.outerRace, "normal", 0.1);
                break;
            case "inner_race_fault":
                applyFaultMaterial(this.innerRace, "inner_race_fault", 0.7);
                this.defectSpot;
                material;
                emissiveIntensity = 1.2;
                break;
            case "outer_race_fault":
                applyFaultMaterial(this.outerRace, "outer_race_fault", 0.7);
                this.defectSpot;
                material;
                emissiveIntensity = 1.0;
                break;
            case "rolling_element_fault":
                this.balls[Math.floor(Math.random() * 9)];
                material;
                emissiveIntensity = 0.8;
                this.defectSpot;
                material;
                emissiveIntensity = 1.0;
                break;
            case "compound_fault":
                applyFaultMaterial(this.innerRace, "compound_fault", 0.5);
                applyFaultMaterial(this.outerRace, "compound_fault", 0.5);
                this.balls[2];
                material;
                emissiveIntensity = 0.6;
                this.defectSpot;
                material;
                emissiveIntensity = 1.0;
                break;
        }
    }
    /** Update animation frame */
    update(deltaTime) {
        this.time += deltaTime;
        const t = this.time;
        // Rotating inner race (shaft speed)
        this.innerRace.rotation.x += 0.025;
        this.cage.rotation.x += deltaTime * 1.5;
        // Balls orbit
        this.ballOrbitGroup.rotation.z += deltaTime * 1.5;
        // Defect spot animation
        const fault = this.faultState.type;
        if (fault === "inner_race_fault") {
            // Defect rotates with the inner race (BPFI pattern)
            this.defectSpot.position.y = 0.39 + Math.sin(t * 0.5) * 0.34;
            this.defectSpot.position.z = Math.cos(t * 0.5) * 0.34;
            this.defectSpot;
            material;
            emissiveIntensity = 0.7 + Math.sin(t * 8) * 0.45;
        }
        else if (fault === "outer_race_fault") {
            // Defect is stationary (BPFO pattern), balls pass over it
            this.defectSpot.position.y = 0.39;
            this.defectSpot.position.z = 0.34;
            this.defectSpot;
            material;
            emissiveIntensity = 0.7 + Math.sin(t * 5) * 0.45;
        }
        else if (fault === "rolling_element_fault") {
            // Defect orbits with ball (BSF pattern)
            this.defectSpot.position.y = Math.sin(t * 0.8) * 0.56;
            this.defectSpot.position.z = Math.cos(t * 0.8) * 0.56;
            this.defectSpot;
            material;
            emissiveIntensity = 0.7 + Math.sin(t * 7) * 0.5;
        }
        else if (fault === "compound_fault") {
            this.defectSpot.position.y = Math.sin(t * 0.6) * 0.4;
            this.defectSpot.position.z = Math.cos(t * 0.6) * 0.4;
            this.defectSpot;
            material;
            emissiveIntensity = 0.8 + Math.sin(t * 6) * 0.6;
        }
    }
}
