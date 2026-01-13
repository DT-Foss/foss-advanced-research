install:
	@echo "Installing dependencies for All Modules..."
	pip install -r Portfolio_Optimized/03_Reference_Implementations/FH-SS_UAV_Simulation/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Cyberdefense_Runtime/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Psychoacoustic_Profiler/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Bidirectional_Comm_Arch/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/WASM_Polyglot/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Multisensory_Projection/requirements.txt
	# Phase 7 Expansion
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Interplanetary_Network_Analyzer/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Maritime_Aero_Tracker/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/ICS_SCADA_Fingerprinter/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Quantum_Network_Mapper/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Hardware_Trust_Anchor/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Algorithmic_Arbitrage_Engine/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Quantitative_Risk_Engine/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Autonomous_OSINT_Platform/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Causal_Knowledge_Graph/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Synthetic_Data_Factory/requirements.txt

test:
	@echo "Running verification tests..."
	python Portfolio_Optimized/03_Reference_Implementations/FH-SS_UAV_Simulation/simulation.py
	# Add unit tests here later

demo:
	@echo "🚀 Running Full Portfolio Demo (16 Modules)..."
	python Portfolio_Optimized/03_Reference_Implementations/FH-SS_UAV_Simulation/simulation.py
	python Portfolio_Optimized/03_Reference_Implementations/Cyberdefense_Runtime/gan_policy.py
	python Portfolio_Optimized/03_Reference_Implementations/Psychoacoustic_Profiler/profiler.py
	python Portfolio_Optimized/03_Reference_Implementations/Bidirectional_Comm_Arch/nfmi_physics.py
	python Portfolio_Optimized/03_Reference_Implementations/WASM_Polyglot/container.py
	python Portfolio_Optimized/03_Reference_Implementations/Multisensory_Projection/projection_sim.py
	python Portfolio_Optimized/03_Reference_Implementations/Interplanetary_Network_Analyzer/dtn_analyzer.py
	python Portfolio_Optimized/03_Reference_Implementations/Maritime_Aero_Tracker/tracker_sim.py
	python Portfolio_Optimized/03_Reference_Implementations/ICS_SCADA_Fingerprinter/ics_scanner.py
	python Portfolio_Optimized/03_Reference_Implementations/Quantum_Network_Mapper/qkd_mapper.py
	python Portfolio_Optimized/03_Reference_Implementations/Hardware_Trust_Anchor/tpm_attestation.py
	python Portfolio_Optimized/03_Reference_Implementations/Algorithmic_Arbitrage_Engine/arbitrage_engine.py
	python Portfolio_Optimized/03_Reference_Implementations/Quantitative_Risk_Engine/risk_engine_var.py
	python Portfolio_Optimized/03_Reference_Implementations/Autonomous_OSINT_Platform/osint_graph_builder.py
	python Portfolio_Optimized/03_Reference_Implementations/Causal_Knowledge_Graph/causal_inference.py
	python Portfolio_Optimized/03_Reference_Implementations/Synthetic_Data_Factory/synthetic_pipeline.py
	@echo "✅ Demos Verification Complete. Check 03_Reference_Implementations/ for generated PNGs."

clean:
	@echo "Cleaning up generated artifacts..."
	find . -name "*.png" -delete
	find . -name "__pycache__" -delete
