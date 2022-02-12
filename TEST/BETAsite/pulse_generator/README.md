# Pulse generator
A python package to generate pulse operating on Qubit 
The operation setting in script:

function/parameter1/parameter2...,duration,amplitude
## functions
f(x): x from 0 to T
duration: T - the duration of this function
amplitude: A - the prefactor used to scale function 
### Linear series
#### flat
<img src="https://render.githubusercontent.com/render/math?math=f(x)=A">

### gauss series
<img src="https://render.githubusercontent.com/render/math?math=f(x) = Ae^{-\frac{1}{2}(\frac{(x-x_0)}{\sigma}^2) }">
p1: sfactor - the factor devide length will get the sigma of gaussian function

####  gauss

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{sfactor}"><img src="https://render.githubusercontent.com/render/math?math=x_0 = \frac{T}{2}">

#### gaussup

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{2T}{sfactor}"><img src="https://render.githubusercontent.com/render/math?math=x_0 = T">

#### gaussdn

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{2T}{sfactor}"><img src="https://render.githubusercontent.com/render/math?math=x_0 = 0">


### derivative gauss series
<img src="https://render.githubusercontent.com/render/math?math=f(x) = \frac{A}{\sigma^2}(x-x0)e^{-\frac{1}{2}(\frac{(x-x_0)}{\sigma}^2) }">
p1: sfactor - the factor devide length will get the sigma of gaussian function

#### gauss

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{sfactor}"><img src="https://render.githubusercontent.com/render/math?math=x_0 = \frac{T}{2}">

#### gaussup

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{2T}{sfactor}"><img src="https://render.githubusercontent.com/render/math?math=x_0 = T">

#### gaussdn

<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{2T}{sfactor}">
<img src="https://render.githubusercontent.com/render/math?math=x_0 = 0">


### drag
<img src="https://render.githubusercontent.com/render/math?math=f(x) = e^{i\theta }(Ae^{-\frac{1}{2}(\frac{x-x_0}{\sigma})^2} +iB\frac{(x-x0)}{\sigma^2}e^{-\frac{1}{2}(\frac{x-x_0}{\sigma})^2 })">
<img src="https://render.githubusercontent.com/render/math?math=\sigma = \frac{T}{sfactor}">
<img src="https://render.githubusercontent.com/render/math?math=x_0 = \frac{T}{2}">
<img src="https://render.githubusercontent.com/render/math?math=B = A\time ">

p1: sfactor - the factor devide length will get the sigma of gaussian function
p2: dratio - 
p3: angle of rotation axis - in angle unit
