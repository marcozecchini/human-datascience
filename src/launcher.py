import matlab.engine

eng = matlab.engine.start_matlab()
print("MATLAB engine started")
eng.modelTrainer(nargout=0)
print("Operation Completed.")
