class Solution(object):
    def maximumRequests(self, n, requests):
        req=requests
        sum=0
        for i in requests:
            if i[0]==i[1]:
                req.remove(i)
                sum+=1
        print(req)

        for i in range(0,n):
            counter=0
            for j in req:
                if j[0]==i:
                    counter+=1
            maxi=counter
            for j in req:
                if j[1]==i and counter!=0:
                    counter-=1
            maxi=maxi-counter
            
            sum=sum+maxi
           

        return sum


requests =[[0,0],[1,1],[0,0],[2,0],[2,2],[1,1],[2,1],[0,1],[0,1]]
n=3
print(Solution().maximumRequests(n,requests))