from manim import *

# Define custom colors to match the diagram
BG_COLOR = "#EBF5FB"
CLIENT_SIDE_COLOR = "#4DD0E1"  # Teal for the Services box
ASYNC_LAYER_COLOR = "#FFCC80"  # Light Orange
INFRA_TEXT_COLOR = "#37474F"
BOX_PURPLE = "#7E57C2"
BOX_ORANGE = "#FFA726"
BOX_LIME = "#9CCC65"
BOX_YELLOW = "#FFEE58"
BOX_BLUE = "#4FC3F7"
BOX_RED = "#EF5350"
BOX_GREEN = "#A5D6A7"
BOX_LIGHT_GREEN = "#C5E1A5"
DB_BROWN = "#A1887F"


class DistributedSystemDiagram(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # --- Title ---
        title = Text("Distribut System Architecture", font_size=48, color=BLACK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # --- Client Side ---
        client_rect = Rectangle(width=1.5, height=1, color=BOX_ORANGE, fill_opacity=1).next_to(title, DOWN, buff=1.5).to_edge(LEFT, buff=1.5)
        client_text = Text("Client", font_size=24, color=BLACK).move_to(client_rect.get_center())
        client_label = Text("Client Side", font_size=20, color=BLACK).next_to(client_rect, UP)
        client_group = VGroup(client_rect, client_text, client_label)
        self.play(FadeIn(client_group, shift=UP))

        # Forward Proxy (FP)
        fp_rect = Rectangle(width=1.5, height=1, color=BOX_PURPLE, fill_opacity=1).next_to(client_rect, RIGHT, buff=1.2)
        fp_text = Text("FP", font_size=24, color=WHITE).move_to(fp_rect.get_center())
        fp_label = Text("Squid\nEnvoy", font_size=20, color=BLACK).next_to(fp_rect, DOWN)
        fp_group = VGroup(fp_rect, fp_text, fp_label)
        arrow_client_to_fp = Arrow(client_rect.get_right(), fp_rect.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_client_to_fp))
        self.play(Create(fp_rect), Write(fp_text), Write(fp_label))

        # API Gateway (AP)
        ap_rect = Rectangle(width=1.5, height=1, color=BOX_ORANGE, fill_opacity=1).next_to(fp_rect, RIGHT, buff=1.2)
        ap_text = Text("AP", font_size=24, color=WHITE).move_to(ap_rect.get_center())
        ap_label = Text("API Gateway\nZuul\nSpring Gateway", font_size=20, color=BLACK).next_to(ap_rect, DOWN)
        ap_group = VGroup(ap_rect, ap_text, ap_label)
        arrow_fp_to_ap = Arrow(fp_rect.get_right(), ap_rect.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_fp_to_ap))
        self.play(Create(ap_rect), Write(ap_text), Write(ap_label))

        # Reverse Proxy (RP)
        rp_rect = Rectangle(width=1.5, height=1, color=BOX_LIME, fill_opacity=1).next_to(ap_rect, RIGHT, buff=1.2)
        rp_text = Text("RP", font_size=24, color=WHITE).move_to(rp_rect.get_center())
        rp_label = Text("APIGW", font_size=20, color=BLACK).next_to(rp_rect, DOWN)
        rp_group = VGroup(rp_rect, rp_text, rp_label)
        arrow_ap_to_rp = Arrow(ap_rect.get_right(), rp_rect.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_ap_to_rp))
        self.play(Create(rp_rect), Write(rp_text), Write(rp_label))

        # KK (NGINX)
        kk_rect = Rectangle(width=1.5, height=1, color=BOX_YELLOW, fill_opacity=1).next_to(rp_rect, RIGHT, buff=1.2)
        kk_text = Text("KK", font_size=24, color=BLACK).move_to(kk_rect.get_center())
        kk_label = Text("NGINX", font_size=20, color=BLACK).next_to(kk_rect, DOWN)
        kk_group = VGroup(kk_rect, kk_text, kk_label)
        arrow_rp_to_kk = Arrow(rp_rect.get_right(), kk_rect.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_rp_to_kk))
        self.play(Create(kk_rect), Write(kk_text), Write(kk_label))

        # Rate Limiter
        rl_label_main = Text("Rate Limiter", font_size=20, color=BLACK).next_to(ap_label, DOWN, buff=0.2).shift(LEFT*0.5)
        rl_label_tech = Text("RL\nNGINX", font_size=20, color=BLACK).next_to(rp_group, DOWN, buff=0.2).align_to(rl_label_main, UP)
        rl_arrow = Arrow(ap_label.get_bottom(), rl_label_main.get_top(), buff=0.1, color=BLACK)
        self.play(Create(rl_arrow), Write(rl_label_main), Write(rl_label_tech))

       #self.wait(1)

        # --- Services Layer ---
        services_box = Rectangle(width=13, height=3, color=CLIENT_SIDE_COLOR, fill_opacity=1).next_to(client_group, DOWN, buff=3.5).shift(RIGHT*2.5)
        services_title = Text("Services", font_size=24, color=BLACK).set_z_index(1).align_to(services_box, UP).shift(UP*0.3 + LEFT*5)
        self.play(FadeIn(services_box), Write(services_title))

        # Discovery & Routing
        dr_label = Text("Discovery & Routing", font_size=22, color=BLACK).align_to(services_box, UL).shift(RIGHT*0.5 + DOWN*0.5)
        hystrix_shape = RegularPolygon(n=6, color=BOX_YELLOW, fill_opacity=1).scale(0.6).next_to(dr_label, DOWN, buff=0.5).align_to(dr_label, LEFT)
        hystrix_text = Text("Ey", font_size=24, color=BLACK).move_to(hystrix_shape.get_center())
        hystrix_label = Text("Hystrix", font_size=20, color=BLACK).next_to(hystrix_shape, DOWN)
        hystrix_group = VGroup(hystrix_shape, hystrix_text, hystrix_label)
        self.play(Write(dr_label), Create(hystrix_shape), Write(hystrix_text), Write(hystrix_label))
        
        # Service Discovery (SD)
        sd_label = Text("Service Discovery (SD)", font_size=22, color=BLACK).next_to(dr_label, RIGHT, buff=1.0).align_to(dr_label, UP)
        lb_box = Rectangle(width=2.5, height=1, color=BOX_ORANGE, fill_opacity=1).next_to(sd_label, DOWN, buff=0.3).align_to(hystrix_shape, UP)
        lb_text = Text("Load Balancer", font_size=20, color=BLACK).move_to(lb_box.get_center())
        lb_tech_label = Text("Cureka / Istio", font_size=20, color=BLACK).next_to(lb_box, DOWN)
        lb_group = VGroup(lb_box, lb_text, lb_tech_label)
        arrow_hystrix_to_lb = Arrow(hystrix_group.get_right(), lb_group.get_left(), buff=0.1, color=BLACK)
        self.play(Write(sd_label), Create(arrow_hystrix_to_lb), Create(lb_box), Write(lb_text), Write(lb_tech_label))
        
        # Load Balancer (LB)
        lb_title = Text("LB", font_size=22, color=BLACK).next_to(sd_label, RIGHT, buff=2.0).align_to(sd_label, UP)
        nginx_box = Rectangle(width=2.5, height=1, color=BOX_BLUE, fill_opacity=1).next_to(lb_title, DOWN, buff=0.3).align_to(lb_box, UP)
        nginx_text = Text("NGINX\nIstio", font_size=20, color=BLACK).move_to(nginx_box.get_center())
        nginx_group = VGroup(nginx_box, nginx_text)
        arrow_lb_to_nginx = Arrow(lb_group.get_right(), nginx_group.get_left(), buff=0.1, color=BLACK)
        self.play(Write(lb_title), Create(arrow_lb_to_nginx), Create(nginx_box), Write(nginx_text))

       # self.wait(1)

        # Focus camera on Services layer
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(services_box.get_center()).scale(1.0), run_time=1)
        self.wait(1)

        # --- Async Layer ---
        async_box = Rectangle(width=13, height=4.5, color=ASYNC_LAYER_COLOR, fill_opacity=1).next_to(services_box, DOWN, buff=0.75)
        async_title = Text("Async Layer", font_size=24, color=BLACK).set_z_index(1).align_to(async_box, UP).shift(UP*0.3 + LEFT*4.5)
        async_inner_box = SurroundingRectangle(async_box, buff=-0.2, color=BLACK)
        self.play(FadeIn(async_box), Create(async_inner_box), Write(async_title))

        # Move camera to show the whole async layer box
        #self.play(self.camera.frame.animate.move_to(async_box.get_center()).scale(1.8), run_time=1)

        # Zoom in and focus on the async layer
        self.play(self.camera.frame.animate.move_to(async_box.get_center()).scale(1.0), run_time=1)

        # Circuit Breaker
        cb1 = Circle(radius=0.5, color=BOX_YELLOW, fill_opacity=1).move_to(async_box.get_center() + LEFT*3 + UP*0.8)
        cb1_text = Text("CB1", font_size=24, color=BLACK).move_to(cb1.get_center())
        cb_group = VGroup(cb1, cb1_text)
        self.play(Create(cb1), Write(cb1_text))

        # Services
        user_service = Rectangle(width=1.8, height=1, color=BOX_LIME).next_to(cb_group, DOWN, buff=0.6).shift(LEFT*1)
        user_text = Text("User\nService", font_size=18, color=BLACK).move_to(user_service.get_center())
        order_service1 = user_service.copy().set_color(BOX_ORANGE).next_to(user_service, RIGHT)
        order_text1 = Text("Order\nService", font_size=18, color=BLACK).move_to(order_service1.get_center())
        
        
        
        arrow_cb_to_user = Arrow(cb_group.get_bottom(), user_service.get_top(), buff=0.5, color=BLACK)
        s1_label_user = Text("$1", font_size=20, color=BLACK).next_to(arrow_cb_to_user, LEFT)
        arrow_cb_to_order1 = Arrow(cb_group.get_bottom(), order_service1.get_top(), buff=0.5, color=BLACK)
        s1_label_order = Text("$1", font_size=20, color=BLACK).next_to(arrow_cb_to_order1, RIGHT)
        self.play(Create(arrow_cb_to_user), Write(s1_label_user), Create(arrow_cb_to_order1), Write(s1_label_order))
       
        self.play(Create(user_service), Write(user_text))
        self.play(Create(order_service1), Write(order_text1 ))
        # Message Queues and more services
        mq1 = Rectangle(width=1.5, height=0.7, color=BOX_RED).next_to(cb_group, RIGHT, buff=1.0).align_to(cb_group, UP)
        mq1_text = Text("MQ", font_size=24, color=WHITE).move_to(mq1.get_center())
        mq2 = mq1.copy().set_color(BOX_BLUE).next_to(mq1, RIGHT, buff=2.5)
        mq2_text = Text("MQ", font_size=24, color=WHITE).move_to(mq2.get_center())
        
        arrow_cb_to_mq1 = Arrow(cb_group.get_right(), mq1.get_left(), buff=0.1, color=BLACK)
        arrow_mq1_to_mq2 = Arrow(mq1.get_right(), mq2.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_cb_to_mq1), Create(mq1), Write(mq1_text))
        self.play(Create(arrow_mq1_to_mq2), Create(mq2), Write(mq2_text))

        order_service2 = order_service1.copy().next_to(mq1, DOWN, buff=1.1).align_to(mq1, LEFT)
        order_text2 = Text("Order\nService", font_size=18, color=BLACK).move_to(order_service2.get_center())
        inventory_service1 = user_service.copy().set_color(BOX_BLUE).next_to(mq2, DOWN, buff=1.1).shift(LEFT*1)
        inventory_text1 = Text("Inventory\nService", font_size=18, color=BLACK).move_to(inventory_service1.get_center())
        inventory_service2 = inventory_service1.copy().set_color(BOX_LIGHT_GREEN).next_to(inventory_service1, RIGHT)
        inventory_text2 = Text("Inventory\nService", font_size=18, color=BLACK).move_to(inventory_service2.get_center())
        
        arrow_mq1_to_order = Arrow(mq1.get_bottom(), order_service2.get_top(), buff=0.1, color=BLACK)
        s2_label = Text("$2", font_size=20, color=BLACK).next_to(arrow_mq1_to_order, LEFT)
        arrow_mq2_to_inv1 = Arrow(mq2.get_bottom(), inventory_service1.get_top(), buff=0.1, color=BLACK)
        s3_label1 = Text("$3", font_size=20, color=BLACK).next_to(arrow_mq2_to_inv1, LEFT)
        arrow_mq2_to_inv2 = Arrow(mq2.get_bottom(), inventory_service2.get_top(), buff=0.1, color=BLACK)
        s3_label2 = Text("$3", font_size=20, color=BLACK).next_to(arrow_mq2_to_inv2, RIGHT)

        self.play(Create(arrow_mq1_to_order), Create(order_service2), Write(order_text2), Write(s2_label))
        self.play(
            Create(arrow_mq2_to_inv1), Create(inventory_service1), Write(inventory_text1), Write(s3_label1),
            Create(arrow_mq2_to_inv2), Create(inventory_service2), Write(inventory_text2), Write(s3_label2)
        )
        self.wait(1)

        # Focus camera on Async Layer
        self.play(self.camera.frame.animate.move_to(async_box.get_center()).scale(1.9), run_time=1)
        self.wait(1)

        # --- Infra Layer ---
        infra_box = Rectangle(
            width=13,
            height=6,
            color=BOX_LIGHT_GREEN,
            fill_opacity=0.2,
            stroke_opacity=0.7
        ).next_to(async_box, DOWN, buff=0.5)
        infra_title = Text("Infra", font_size=32, color=BLACK).next_to(infra_box, UP, buff=0.3).align_to(infra_box, LEFT).shift(LEFT*1)
        self.play(FadeIn(infra_box), Write(infra_title))
        self.play(self.camera.frame.animate.move_to(infra_box.get_center()).scale(1.0), run_time=1)

        # Center Kafka horizontally in infra_box
        kafka_db = Rectangle(width=2.2, height=1, color=DB_BROWN, fill_opacity=1).move_to(infra_box.get_center() + UP*0.7)
        kafka_label = Text("Kafka", font_size=24, color=BLACK).move_to(kafka_db.get_center())
        mq_label = Text("MQ  Message Broker", font_size=22, color=BLACK).next_to(kafka_db, UP, buff=0.2)
        self.play(Write(mq_label), Create(kafka_db), Write(kafka_label))

        # Arrange infra components in a row below Kafka
        cfg_db = Rectangle(width=1.8, height=0.8, color=BOX_GREEN, fill_opacity=1).next_to(kafka_db, DOWN, buff=1.0).shift(LEFT*4)
        cfg_icon = Text("✳", color=YELLOW, font_size=24).move_to(cfg_db.get_center())
        cfg_text_label = Text("CFG", font_size=24, color=BLACK).move_to(cfg_db.get_center() + DOWN*0.3)
        cfg_desc = Text("Central Server", font_size=20, color=BLACK).next_to(cfg_db, DOWN)
        cfg_group = VGroup(cfg_db, cfg_icon, cfg_text_label, cfg_desc)

        mon_rect = Rectangle(width=1.5, height=0.8, color=BOX_BLUE, fill_opacity=1).next_to(kafka_db, DOWN, buff=1.0).shift(LEFT*1.5)
        mon_text = Text("MON", font_size=18, color=WHITE).move_to(mon_rect.get_center())
        mon_label = Text("Prometheus\nGrafana", font_size=20, color=BLACK).next_to(mon_rect, DOWN)
        mon_title = Text("MON", font_size=24, color=BLACK).next_to(mon_rect, UP, buff=0.3)
        mon_group = VGroup(mon_rect, mon_text, mon_label, mon_title)

        log_rect = Rectangle(width=1.5, height=1.0, color=BOX_YELLOW, fill_opacity=1).next_to(kafka_db, DOWN, buff=1.0).shift(RIGHT*1.5)
        log_text = Text("ELL", font_size=18, color=BLACK).move_to(log_rect.get_center())
        log_label = Text("Central Logging\nELK", font_size=20, color=BLACK).next_to(log_rect, DOWN)
        log_title = Text("LOG", font_size=24, color=BLACK).next_to(log_rect, UP, buff=0.3)
        log_group = VGroup(log_rect, log_text, log_label, log_title)

        trace_rect = Rectangle(width=1.5, height=0.8, color=CLIENT_SIDE_COLOR, fill_opacity=1).next_to(kafka_db, DOWN, buff=1.0).shift(RIGHT*4)
        trace_text = Text("eLit", font_size=18, color=BLACK).move_to(trace_rect.get_center())
        trace_label = Text("Jaeger\nZipkin", font_size=20, color=BLACK).next_to(trace_rect, DOWN)
        trace_title = Text("TRACE", font_size=24, color=BLACK).next_to(trace_rect, UP, buff=0.3)
        trace_group = VGroup(trace_rect, trace_text, trace_label, trace_title)

        self.play(FadeIn(cfg_group, shift=UP))
        self.play(FadeIn(mon_group, shift=UP))
        self.play(FadeIn(log_group, shift=UP))
        self.play(FadeIn(trace_group, shift=UP))

        # Infra Connections (adjusted for new positions)
        arrow_kafka_to_cfg = Arrow(kafka_db.get_bottom(), cfg_db.get_top(), buff=0.1, color=BLACK)
        arrow_kafka_to_mon = Arrow(kafka_db.get_bottom(), mon_rect.get_top(), buff=0.1, color=BLACK)
        arrow_kafka_to_log = Arrow(kafka_db.get_bottom(), log_rect.get_top(), buff=0.1, color=BLACK)
        arrow_kafka_to_trace = Arrow(kafka_db.get_bottom(), trace_rect.get_top(), buff=0.1, color=BLACK)
        arrow_cfg_to_mon = Arrow(cfg_db.get_right(), mon_rect.get_left(), buff=0.1, color=BLACK)

        # ELK text for log
        elk_text = Text("ELK", font_size=20, color=BLACK).next_to(arrow_kafka_to_log.get_center(), UP, buff=0.01).shift(LEFT*0.5)

        self.play(
            Create(arrow_kafka_to_cfg),
            Create(arrow_cfg_to_mon),
            Create(arrow_kafka_to_mon),
            Create(arrow_kafka_to_log), Write(elk_text),
            Create(arrow_kafka_to_trace)
        )
        self.wait(1)

        # (No further camera movement; stay focused on infra layer)