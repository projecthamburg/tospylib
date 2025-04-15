from enum import Enum

class FundamentalType(Enum):
    CLOSE = "Close"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"

class AggregationPeriod(Enum):
    DAY = "1D"
    THREE_DAYS = "3D"
    WEEK = "1W"
    MONTH = "1M"

class AverageType(Enum):
    SIMPLE = "simple"
    EXPONENTIAL = "exponential"
    WEIGHTED = "weighted"
    WILDERS = "wilders"
    HULL = "hull"
