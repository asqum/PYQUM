# Pulse generator
A python package to generate pulse operating on Qubit 
The operation setting in script:

function/parameter1,parameter2...
## functions
f(x): x from 0 to T
p2: A - the prefactor used to scale function 
p3: T - the duration of this function
### Linear series
command: flat

<img src="https://render.githubusercontent.com/render/math?math=f(x)=p_2">
p1: dummy - keep empty

### gauss series
<img src="https://render.githubusercontent.com/render/math?math=f(x) = Ae^{-\frac{1}{2}(\frac{(x-x_0)}{\sigma}^2) }">
p1: sfactor - the factor devide length will get the sigma of gaussian function

command: gauss

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{sfactor}">
<img src="https://render.githubusercontent.com/render/math?math=x_0 = \frac{T}{2}">

command: gaussup

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{2*sfactor}">
<img src="https://render.githubusercontent.com/render/math?math=x_0 = T">

command: gaussdn

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{2*sfactor}">
<img src="https://render.githubusercontent.com/render/math?math=x_0 = 0">


### dgauss
p1: sfactor - the factor/2 devide length will get the sigma of gaussian function

### dgaussup, dgaussdn
p1: sfactor - the factor/2 devide length will get the sigma of gaussian function


### drag
