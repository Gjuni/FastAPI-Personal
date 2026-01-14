from src.model.threadModel import testModel

async def testServcie() :
    value = await testModel()
    return value
