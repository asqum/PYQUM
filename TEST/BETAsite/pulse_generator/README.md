# Pulse generator
A python package to generate pulse operating on Qubit 
The operation setting in script:

function/parameter1,parameter2...
## functions
p2: amplitude - the prefactor used to scale function 
p3: length - the duration of this function
### flat
<img src="https://render.githubusercontent.com/render/math?math=f(x)=p2">
p1: dummy - keep empty

### gauss
f(x) = amplitude * exp( -1/2*((x-x0)/sigma)^2 )
p1: sfactor - the factor devide length will get the sigma of gaussian function
p2: amplitude - the value of constant output voltage 
p3: length - the duration of this function
### gaussup, gaussdn
p1: sfactor - the factor/2 devide length will get the sigma of gaussian function
p2: amplitude - the value of constant output voltage 
p3: time - the length of this function
### dgauss
p1: sfactor - the factor/2 devide length will get the sigma of gaussian function
p2: amplitude - the value of constant output voltage 
p3: time - the length of this function
### dgaussup, dgaussdn
p1: sfactor - the factor/2 devide length will get the sigma of gaussian function
p2: amplitude - the value of constant output voltage 
p3: time - the length of this function
gaussup/ sfactor, amplitude, time
gaussdn/ get_gaussdn,
'dgauss': get_dgauss,
'dgaussup': get_dgaussup,
'dgaussdn': get_dgaussdn,
'drag': get_drag,