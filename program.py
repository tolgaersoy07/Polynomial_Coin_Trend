import json
import matplotlib.pyplot
import numpy
import requests
def calculate(array,x):
	return numpy.polyval(array,x)
def coefficients(X,Y,n):
	A=numpy.linalg.inv(numpy.array(equation1(X,n+1)))
	B=numpy.array(equation2(X,Y,n+1))
	return numpy.dot(A,B)
def control(coin,time,limit):
    url="https://api.binance.com/api/v3/klines?symbol="+coin+"&interval="+time+"&limit="+str(limit)
    data=requests.get(url).json()
    if len(data)!=limit:
        return len(data)
    return limit
def equation1(array,n):
	data=[sumpower(array,i) for i in range((2*n)-1)]
	matrix=numpy.zeros((n,n))
	for i in range(n):
		for j in range(n):
			matrix[i][j]=data[i+j]
	return matrix
def equation2(X,Y,n):
	return [multiplypower(X,Y,i) for i in range(n)]
def errorcalculate(Y,Y1,p):
	t=0
	for i in range(p):
		t+=abs(Y[i]-Y1[i])
	return 100*((t)/(p*Y[-1]))
def getdata(coin,time,limit):
    url="https://api.binance.com/api/v3/klines?symbol="+coin+"&interval="+time+"&limit="+str(limit)
    data=requests.get(url).json()
    output=[]
    for i in data:
    	output.append(((float(i[1])+float(i[2])+float(i[3])+float(i[4]))/(4)))
    return output
def graphic(X,Y,n,p,f):
	matplotlib.pyplot.plot(X,Y)
	array=coefficients(X,Y,n)[::-1]
	polynomial(array,f)
	Y1=[calculate(array,i) for i in X]
	matplotlib.pyplot.plot(X,Y1)
	matplotlib.pyplot.show()
def minerrorcalculate(X,Y):
	Y1=[calculate(coefficients(X,Y,0)[::-1],j) for j in X]
	error=errorcalculate(Y,Y1,X[-1])
	degree=0
	print("\n0. polynomial degree error: %"+str(round(error,4)))
	for i in range(1,16):
		Y1=[calculate(coefficients(X,Y,i)[::-1],j) for j in X]
		t=errorcalculate(Y,Y1,X[-1])
		print(str(i)+". polynomial degree error: %",round(t,4))
		if t<error:
			error=t
			degree=i
	print("\nMinimum error: %",round(error,4))
	print("Minimum errors polynomial degree: "+str(degree))
	print("\nThe calculated value is approximately %"+str(round(error,4))+" away from the real value.")
	return degree
def multiplypower(X,Y,n):
	t=0
	for i in range(len(X)):
		t+=Y[i]*X[i]**n
	return t
def polynomial(array,f):
	print("\nBlue: Real values.\nOrange: Calculated values.\n")
	result="P(x) = "
	for i in range(len(array)):
		result+="("+str(round(abs(array[i]),f))+"*X^"+str(i)+")"
		if i+1<len(array):
			if array[i+1]>=0:
				result+=" + "
			else:
				result+=" - "
	print(result)
def run(p,c,t,f):
	X=[i for i in range(p)]
	Y=getdata(c,t,p)
	graphic(X,Y,minerrorcalculate(X,Y),p,f)
def sumpower(array,n):
	t=0
	for i in array:
		t+=i**n 
	return t
def main():
	#User just must be set following values. -> [c,f,t,p]
	c=input("Enter the coin name: ")# Coin name. Coin list -> https://www.binance.com/en/markets/spot_margin-USDT
	f=int(input("Enter the decimal tolerance: ")) # Number of digits after comma to coefficients of polynomial.
	t=input("Enter the graphic time: ") # Graphic time. -> (1s,1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M)
	p=control(c,t,int(input("Enter the number of points: "))) # Number of points to use.
	run(p,c,t,f)
main()
print("\nProgram closed.")