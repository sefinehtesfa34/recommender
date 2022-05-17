from .preProcessorModel import PopularityRecommender

class PredictorClass:
    def __init__(self) -> None:    
        popular=PopularityRecommender()
        popular.printer()
    

