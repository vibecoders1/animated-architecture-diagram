from manim import *

class DistributedSystemFullDiagram(MovingCameraScene):
    def construct(self):
        title = Text("Distributed Microservices System Architecture", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Client App
        client = Rectangle(width=2.5, height=1, color=BLUE).shift(LEFT * 5 + UP * 2)
        client_text = Text("Client App", font_size=24).move_to(client.get_center())
        self.play(Create(client), Write(client_text))

        # Forward Proxy
        forward_proxy = Rectangle(width=2.5, height=1, color=ORANGE).next_to(client, RIGHT, buff=0.8)
        forward_proxy_text = Text("Forward Proxy", font_size=20).move_to(forward_proxy.get_center())
        self.play(Create(forward_proxy), Write(forward_proxy_text))
        self.play(Create(Arrow(client.get_right(), forward_proxy.get_left(), buff=0.1)))

        # API Gateway
        gateway = Rectangle(width=2.5, height=1, color=YELLOW).next_to(forward_proxy, RIGHT, buff=0.8)
        gateway_text = Text("API Gateway", font_size=20).move_to(gateway.get_center())
        self.play(Create(gateway), Write(gateway_text))
        self.play(Create(Arrow(forward_proxy.get_right(), gateway.get_left(), buff=0.1)))

        # Rate Limiter
        rate_limiter = Rectangle(width=2, height=1, color=RED).next_to(gateway, DOWN, buff=1)
        rate_limiter_text = Text("Rate Limiter", font_size=18).move_to(rate_limiter.get_center())
        self.play(Create(rate_limiter), Write(rate_limiter_text))
        self.play(Create(Arrow(gateway.get_bottom(), rate_limiter.get_top(), buff=0.1)))

        # Reverse Proxy
        reverse_proxy = Rectangle(width=2.5, height=1, color=PURPLE).next_to(gateway, RIGHT, buff=0.8)
        reverse_proxy_text = Text("Reverse Proxy", font_size=18).move_to(reverse_proxy.get_center())
        self.play(Create(reverse_proxy), Write(reverse_proxy_text))
        self.play(Create(Arrow(gateway.get_right(), reverse_proxy.get_left(), buff=0.1)))

        # Service Discovery
        discovery = Rectangle(width=2.5, height=1, color=GREEN).next_to(reverse_proxy, DOWN, buff=1)
        discovery_text = Text("Service Discovery", font_size=18).move_to(discovery.get_center())
        self.play(Create(discovery), Write(discovery_text))
        self.play(Create(Arrow(reverse_proxy.get_bottom(), discovery.get_top(), buff=0.1)))

        # Load Balancer (below Service Discovery)
        lb = Rectangle(width=2.5, height=1, color=TEAL).next_to(discovery, DOWN, buff=0.7)
        lb_text = Text("Load Balancer", font_size=18).move_to(lb.get_center())
        self.play(Create(lb), Write(lb_text))
        self.play(Create(Arrow(discovery.get_bottom(), lb.get_top(), buff=0.1)))

        # Circuit Breaker (below Load Balancer)
        cb = Rectangle(width=2, height=1, color=MAROON).next_to(lb, DOWN, buff=0.7)
        cb_text = Text("Circuit Breaker", font_size=16).move_to(cb.get_center())
        self.play(Create(cb), Write(cb_text))
        self.play(Create(Arrow(lb.get_bottom(), cb.get_top(), buff=0.1)))

        # Services (horizontally, spaced out, below Circuit Breaker)
        user_service = Rectangle(width=2.5, height=1, color=BLUE_E).next_to(cb, DOWN + LEFT, buff=1.2)
        order_service = Rectangle(width=2.5, height=1, color=BLUE_E).next_to(cb, DOWN, buff=1.2)
        inventory_service = Rectangle(width=2.5, height=1, color=BLUE_E).next_to(cb, DOWN + RIGHT, buff=1.2)

        user_text = Text("User Service", font_size=18).move_to(user_service.get_center())
        order_text = Text("Order Service", font_size=18).move_to(order_service.get_center())
        inventory_text = Text("Inventory Service", font_size=18).move_to(inventory_service.get_center())
        self.play(self.camera.frame.animate.move_to(inventory_service.get_left()), run_time=2)

        self.play(Create(user_service), Write(user_text))
        self.play(Create(order_service), Write(order_text))
        self.play(Create(inventory_service), Write(inventory_text))

        # Connect circuit breaker to services
        self.play(Create(Arrow(cb.get_bottom(), user_service.get_top(), buff=0.1)))
        self.play(Create(Arrow(cb.get_bottom(), order_service.get_top(), buff=0.1)))
        self.play(Create(Arrow(cb.get_bottom(), inventory_service.get_top(), buff=0.1)))

        print("Camera object:", self.camera)
        print("Camera type:", type(self.camera))
        print("Camera has frame:", hasattr(self.camera, 'frame'))
        # Camera movement: pan right to services, then zoom out
        self.camera.frame.save_state()
        self.wait(0.1)
        services_center = order_service.get_center()
        self.play(self.camera.frame.animate.move_to(services_center), run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(1.8).move_to(ORIGIN), run_time=2)
        self.wait(2)