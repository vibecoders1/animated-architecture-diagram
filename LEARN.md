## Important

## Camera movement within frame

```
from manim import *

class DistributedSystemFullDiagram(MovingCameraScene):
    def construct(self):
```

## debug
```
print("Camera object:", self.camera)
print("Camera type:", type(self.camera))
print("Camera has frame:", hasattr(self.camera, 'frame'))
```

## self test
```
from manim import *

class DistributedSystemFullDiagram(Scene):
    def construct(self):
        print("Camera object:", self.camera)
        print("Camera dir:", dir(self.camera))
        title = Text("Distributed Microservices System Architecture", font_size=36).to_edge(UP)
        self.play(Write(title))
```        


```
# Move camera to show the whole async layer box
        self.play(self.camera.frame.animate.move_to(async_box.get_center()).scale(1.8), run_time=1)

```