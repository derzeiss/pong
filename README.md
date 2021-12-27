# pong
Pong game made in python (plus translated to typescript).

What's special about this one is your can write your own AI quite easily.


**Note**: This documentation is written for the python version. Implementing a typescript AI works nearly the same, but has some slight differences. See [Implementing a typescript AI](#implementing-a-typescript-ai) for detailed instructions.

## Writing your own AI
Subclass ``AIBar`` and implement a ``handle_input `` method.
```python
class LowIntelligenceAIBar(AIBar):
    def handle_input(self):
        ball = self.game.ball
        ball_center = ball.y + ball.height // 2
        self_center = self.y + self.height // 2
        if abs(ball_center - self_center) > 5:  # prevent ball flickering
            if ball_center < self_center:
                self.move_up()
            elif ball_center > self_center:
                self.move_down()
```

Initialize ``Game`` with the new class.
```python            
if __name__ == '__main__':
    Game(Bar, LowIntelligenceAIBar).run()
```

## Available properties and methods inside ``handle_input``
There are several members that you can access inside the method.  
You can't change properties directly, you can only call ``move_up()`` and ``move_down()``. If you call none of them, the Bar will do nothing this frame, whatever one you call last will be executed.

**Note:** Calling ``move_up()`` or ``move_down()`` does not stack. So calling them multiple times will only execute them once.  
**Note:** All given coordinates describe the objects upper left corner.

#### self (AIBar)
````
x
y
vx - usually 0
vy
width
height
move_up() - move bar up
move_down() - move bar down
````
#### self.game
````
width - window width
height - window height
````
#### self.game.ball
````
x
y
vx
vy
width
height
````

## Implementing a typescript AI
Now you know how to implement a python AI. Implementing one in typescript works nearly the same, with only a few differences:
- Initializing a game with a new Bar AI works the same, but is done in `~/pong.ts/src/script/index.ts`
- All properties are getters, so instead of `self.x`, use `this.getX()`
- There is a `this.dont_move()` method to prevent the bar from moving, even if `move_up` or `move_down` has already been called.
- Except the getters all methods are still in `snake_case`, even though JS/TS uses `camelCase` by default.


## TODO
* Correct collision when ball hits Bar on top or bottom 
* Prevent ball from "tunneling" through bar at high speeds
* Sound
* *Explosions?*