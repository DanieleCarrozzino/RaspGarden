from ultralytics import YOLO

class PlantAnalyzer():

    # Init yolov8 model
    def __init__(self) -> None:
        self.model = YOLO('best.pt')

    def getWebcamResult(self):
        result = self.model(source = 0, show = True, conf = 0.4, save = True)
        print(result)
        pass

    pass