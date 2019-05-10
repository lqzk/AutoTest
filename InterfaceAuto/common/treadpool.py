import threadpool

class ThreadPool:
    def __init__(self,func,pool_size,data):
        self.func=func
        self.pool_size=pool_size
        self.data=data

    def pool(self):
        pool=threadpool.ThreadPool(self.pool_size)
        reqs=threadpool.makeRequests(self.func,self.data)
        for req in reqs:
            print("start", req)
            pool.putRequest(req)
            pool.wait()



        # [pool.putRequest(req)  for req in reqs]


