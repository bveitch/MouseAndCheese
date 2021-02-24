# MouseAndCheese

A simulated mouse moves around a 2D world looking for cheese, by taking random steps from a list of directions, 'left', 'right', 'up', 'down'.
The mouse has a limited memory bank of previous steps taken and the smell of the cheese at each step. The 'smell' acts as a proximity sensor and is modelled as a 1/r^2 model  The mouse has no knowledge of its location or that of the cheese.

At the first iteration the step weights are all equal. However, as memories are accumulated these weights are updated, and the mouse will begin to converge to the cheese. The program will break on success.
