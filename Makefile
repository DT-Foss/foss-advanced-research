install:
	@echo "Installing dependencies..."
	pip install -r Portfolio_Optimized/03_Reference_Implementations/FH-SS_UAV_Simulation/requirements.txt
	pip install -r Portfolio_Optimized/03_Reference_Implementations/Psychoacoustic_Profiler/requirements.txt
	# Add any other requirement files here

test:
	@echo "Running UAV Simulation Test..."
	python Portfolio_Optimized/03_Reference_Implementations/FH-SS_UAV_Simulation/simulation.py

demo:
	@echo "🚀 Running Portfolio Demos..."
	@echo "1. Generating Chaos Attractor (Cyberdefense)..."
	python Portfolio_Optimized/03_Reference_Implementations/Cyberdefense_Runtime/gan_policy.py
	@echo "2. Generating EEG Spectrum (Psychoacoustics)..."
	python Portfolio_Optimized/03_Reference_Implementations/Psychoacoustic_Profiler/profiler.py
	@echo "3. Generating HDC Stability Plot (Multisensory)..."
	python Portfolio_Optimized/03_Reference_Implementations/Multisensory_Projection/projection_sim.py
	@echo "✅ Demos Verification Complete. Check 03_Reference_Implementations/ for generated PNGs."

clean:
	@echo "Cleaning up generated artifacts..."
	find . -name "*.png" -delete
	find . -name "__pycache__" -delete
