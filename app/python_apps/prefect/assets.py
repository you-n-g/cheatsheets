from prefect import flow
from prefect.assets import materialize

# 定义一个“原始数据”资产
@materialize("file://./a.csv")
def raw_data() -> list[int]:
    print("生成原始数据...")
    return [1, 2, 3, 4, 5]

# 定义一个依赖于 raw_data 的资产
@materialize("file://./b.csv")
def cleaned_data(raw_data: list[int]) -> list[int]:
    print("清洗数据...")
    return [x for x in raw_data if x % 2 == 1]

# 定义一个依赖于 cleaned_data 的资产
@materialize("file://./c.csv")
def stats(cleaned_data: list[int]) -> dict:
    print("统计数据...")
    return {"count": len(cleaned_data), "sum": sum(cleaned_data)}

# 定义一个 flow 调用所有资产
@flow
def asset_pipeline():
    # materialize 表示“计算或读取缓存的资产”
    stats(cleaned_data(raw_data()))

if __name__ == "__main__":
    asset_pipeline()
