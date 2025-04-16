from enum import Enum

class FundamentalType(Enum):
    CLOSE = "Close"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    VOLUME = "Volume"

class AggregationPeriod(Enum):
    MINUTE = "1min"
    FIVE_MIN = "5min"
    FIFTEEN_MIN = "15min"
    HOUR = "1H"
    DAY = "1D"
    WEEK = "1W"
    MONTH = "1M"

class AverageType(Enum):
    SIMPLE = "simple"
    EXPONENTIAL = "exponential"
    WEIGHTED = "weighted"
    WILDERS = "wilders"
    HULL = "hull"
