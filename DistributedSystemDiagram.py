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


class DistributedSystemDiagram(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # --- Title ---
        title = Text("Distribut System Architecture", font_size=48, color=BLACK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # --- Client Side ---
        client_side_title = Text("Client Side", font_size=32, color=BLACK).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(client_side_title))

        # Client
        client_icon = VGroup(
            Circle(radius=0.3, color=BOX_ORANGE, fill_opacity=1).shift(UP*0.2),
            Rectangle(width=0.8, height=0.5, color=BLUE, fill_opacity=1).shift(DOWN*0.25)
        ).scale(0.8).move_to(client_side_title.get_center() + RIGHT*0.5 + DOWN*1.5)
        client_label = Text("Client", font_size=24, color=BLACK).next_to(client_icon, DOWN)
        client_group = VGroup(client_icon, client_label)
        self.play(FadeIn(client_group, shift=UP))
        
        # Forward Proxy (FP)
        fp_shape = RegularPolygon(n=6, color=BOX_PURPLE, fill_opacity=1).scale(0.6).next_to(client_group, RIGHT, buff=1.2)
        fp_text_inner = Text("FP", font_size=24, color=WHITE).move_to(fp_shape.get_center())
        fp_label = Text("Squid\nEnvoy", font_size=20, color=BLACK).next_to(fp_shape, DOWN)
        fp_group = VGroup(fp_shape, fp_text_inner, fp_label)
        
        arrow_client_to_fp = Arrow(client_group.get_right(), fp_group.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_client_to_fp))
        self.play(Create(fp_shape), Write(fp_text_inner), Write(fp_label))

        # API Gateway (AP)
        ap_shape = RegularPolygon(n=6, color=BOX_ORANGE, fill_opacity=1).scale(0.6).next_to(fp_group, RIGHT, buff=2.5).shift(UP*0.8)
        ap_text_inner = Text("AP", font_size=24, color=WHITE).move_to(ap_shape.get_center())
        ap_box = Rectangle(width=2.5, height=0.7, color=BOX_BLUE).next_to(ap_shape, DOWN, buff=0.2)
        ap_box_text = Text("API Gateway", font_size=20, color=BLACK).move_to(ap_box.get_center())
        ap_label = Text("Zuul\nSpring Gateway", font_size=20, color=BLACK).next_to(ap_box, DOWN)
        ap_group = VGroup(ap_shape, ap_text_inner, ap_box, ap_box_text, ap_label)

        arrow_fp_to_ap = Arrow(fp_group.get_right(), ap_box.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_fp_to_ap))
        self.play(Create(ap_shape), Write(ap_text_inner), Create(ap_box), Write(ap_box_text), Write(ap_label))

        # Reverse Proxy (RP) and NGINX (KK)
        apigw_shape = RegularPolygon(n=6, color=BOX_LIME, fill_opacity=1).scale(0.7).next_to(ap_box, RIGHT, buff=1.0)
        apigw_text_inner = Text("RP", font_size=24, color=WHITE).move_to(apigw_shape.get_center())
        apigw_label = Text("APIGW", font_size=20, color=BLACK).next_to(apigw_shape, DOWN)
        apigw_group = VGroup(apigw_shape, apigw_text_inner, apigw_label)

        kk_shape = RegularPolygon(n=6, color=BOX_YELLOW, fill_opacity=1).scale(0.7).next_to(apigw_group, RIGHT, buff=1.0)
        kk_text_inner = Text("KK", font_size=24, color=BLACK).move_to(kk_shape.get_center())
        kk_label = Text("NGINX", font_size=20, color=BLACK).next_to(kk_shape, DOWN)
        kk_group = VGroup(kk_shape, kk_text_inner, kk_label)
        
        arrow_ap_to_rp = Arrow(ap_box.get_right(), apigw_group.get_left(), buff=0.1, color=BLACK)
        arrow_rp_to_kk = Arrow(apigw_group.get_right(), kk_group.get_left(), buff=0.1, color=BLACK)
        arrow_ap_to_kk = Arrow(ap_shape.get_right(), kk_group.get_top(), buff=0.1, color=BLACK, path_arc=-0.5)

        self.play(Create(arrow_ap_to_rp), Create(arrow_ap_to_kk))
        self.play(Create(apigw_shape), Write(apigw_text_inner), Write(apigw_label))
        self.play(Create(arrow_rp_to_kk))
        self.play(Create(kk_shape), Write(kk_text_inner), Write(kk_label))

        # Rate Limiter
        rl_label_main = Text("Rate Limiter", font_size=20, color=BLACK).next_to(ap_label, DOWN, buff=0.2).shift(LEFT*0.5)
        rl_label_tech = Text("RL\nNGINX", font_size=20, color=BLACK).next_to(apigw_group, DOWN, buff=0.2).align_to(rl_label_main, UP)
        rl_arrow = Arrow(ap_label.get_bottom(), rl_label_main.get_top(), buff=0.1, color=BLACK)
        self.play(Create(rl_arrow), Write(rl_label_main), Write(rl_label_tech))

        self.wait(1)

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

        self.wait(1)

        # --- Async Layer ---
        async_box = Rectangle(width=13, height=4.5, color=ASYNC_LAYER_COLOR, fill_opacity=1).next_to(services_box, DOWN, buff=0.75)
        async_title = Text("Async Layer", font_size=24, color=BLACK).set_z_index(1).align_to(async_box, UP).shift(UP*0.3 + LEFT*5.5)
        async_inner_box = SurroundingRectangle(async_box, buff=-0.2, color=BLACK)
        self.play(FadeIn(async_box), Create(async_inner_box), Write(async_title))

        # Circuit Breaker
        cb1 = Circle(radius=0.5, color=BOX_YELLOW, fill_opacity=1).move_to(async_box.get_center() + LEFT*4 + UP*0.8)
        cb1_text = Text("CB1", font_size=24, color=BLACK).move_to(cb1.get_center())
        cb_group = VGroup(cb1, cb1_text)
        self.play(Create(cb1), Write(cb1_text))

        # Services
        user_service = Rectangle(width=1.8, height=1, color=BOX_LIME).next_to(cb_group, DOWN, buff=0.8).shift(LEFT*1)
        user_text = Text("User\nService", font_size=18, color=BLACK).move_to(user_service.get_center())
        order_service1 = user_service.copy().set_color(BOX_ORANGE).next_to(user_service, RIGHT)
        order_text1 = Text("Order\nService", font_size=18, color=BLACK).move_to(order_service1.get_center())
        
        self.play(Create(user_service), Write(user_text))
        self.play(Create(order_service1), Write(order_text1))
        
        arrow_cb_to_user = Arrow(cb_group.get_bottom(), user_service.get_top(), buff=0.1, color=BLACK)
        s1_label_user = Text("$1", font_size=20, color=BLACK).next_to(arrow_cb_to_user, LEFT)
        arrow_cb_to_order1 = Arrow(cb_group.get_bottom(), order_service1.get_top(), buff=0.1, color=BLACK)
        s1_label_order = Text("$1", font_size=20, color=BLACK).next_to(arrow_cb_to_order1, RIGHT)
        self.play(Create(arrow_cb_to_user), Write(s1_label_user), Create(arrow_cb_to_order1), Write(s1_label_order))
        
        # Message Queues and more services
        mq1 = Rectangle(width=1.5, height=0.7, color=BOX_RED).next_to(cb_group, RIGHT, buff=1.0).align_to(cb_group, UP)
        mq1_text = Text("MQ", font_size=24, color=WHITE).move_to(mq1.get_center())
        mq2 = mq1.copy().set_color(BOX_BLUE).next_to(mq1, RIGHT, buff=2.5)
        mq2_text = Text("MQ", font_size=24, color=WHITE).move_to(mq2.get_center())
        
        arrow_cb_to_mq1 = Arrow(cb_group.get_right(), mq1.get_left(), buff=0.1, color=BLACK)
        arrow_mq1_to_mq2 = Arrow(mq1.get_right(), mq2.get_left(), buff=0.1, color=BLACK)
        self.play(Create(arrow_cb_to_mq1), Create(mq1), Write(mq1_text))
        self.play(Create(arrow_mq1_to_mq2), Create(mq2), Write(mq2_text))

        order_service2 = order_service1.copy().next_to(mq1, DOWN, buff=1.1)
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

        # --- Infra Layer ---
        infra_title = Text("Infra", font_size=32, color=BLACK).next_to(async_box, DOWN, buff=1.0).align_to(async_box, LEFT).shift(LEFT*1)
        self.play(Write(infra_title))

        # Kafka (MQ)
        kafka_db = Cylinder(radius=0.8, height=0.5, color=DB_BROWN).next_to(infra_title, RIGHT, buff=1.5)
        kafka_label = Text("Kafka", font_size=24, color=BLACK).next_to(kafka_db, DOWN)
        mq_label = Text("MQ  Message Broker", font_size=22, color=BLACK).align_to(infra_title, UP).align_to(kafka_db, LEFT).shift(UP*0.5)
        self.play(Write(mq_label), Create(kafka_db), Write(kafka_label))

        # Infra components
        cfg_db = Cylinder(radius=0.7, height=0.5, color=BOX_GREEN).next_to(kafka_db, DOWN, buff=1.5).shift(LEFT*4)
        cfg_icon = Text("✳", color=YELLOW, font_size=24).move_to(cfg_db.get_center())
        cfg_text_label = Text("CFG", font_size=24, color=BLACK).next_to(cfg_db, UP, buff=0.3)
        cfg_desc = Text("Central Server", font_size=20, color=BLACK).next_to(cfg_db, DOWN)
        cfg_group = VGroup(cfg_db, cfg_icon, cfg_text_label, cfg_desc)
        
        mon_circle = Circle(radius=0.4, color=BOX_BLUE, fill_opacity=1).next_to(cfg_group, RIGHT, buff=1.0)
        mon_text = Text("MON", font_size=18, color=WHITE).move_to(mon_circle.get_center())
        mon_label = Text("Prometheus\nGrafana", font_size=20, color=BLACK).next_to(mon_circle, DOWN)
        mon_title = Text("MON", font_size=24, color=BLACK).next_to(mon_circle, UP, buff=0.3)
        mon_group = VGroup(mon_circle, mon_text, mon_label, mon_title)

        log_circle = Circle(radius=0.4, color=BOX_YELLOW, fill_opacity=1).next_to(mon_group, RIGHT, buff=2.0)
        log_text = Text("ELL", font_size=18, color=BLACK).move_to(log_circle.get_center())
        log_label = Text("Central Logging\nELK", font_size=20, color=BLACK).next_to(log_circle, DOWN)
        log_title = Text("LOG", font_size=24, color=BLACK).next_to(log_circle, UP, buff=0.3)
        log_group = VGroup(log_circle, log_text, log_label, log_title)

        trace_circle = Circle(radius=0.4, color=CLIENT_SIDE_COLOR, fill_opacity=1).next_to(log_group, RIGHT, buff=2.0)
        trace_text = Text("eLit", font_size=18, color=BLACK).move_to(trace_circle.get_center())
        trace_label = Text("Jaeger\nZipkin", font_size=20, color=BLACK).next_to(trace_circle, DOWN)
        trace_title = Text("TRACE", font_size=24, color=BLACK).next_to(trace_circle, UP, buff=0.3)
        trace_group = VGroup(trace_circle, trace_text, trace_label, trace_title)

        self.play(FadeIn(cfg_group, shift=UP))
        self.play(FadeIn(mon_group, shift=UP))
        self.play(FadeIn(log_group, shift=UP))
        self.play(FadeIn(trace_group, shift=UP))

        # Infra Connections
        arrow_kafka_to_cfg = Arrow(kafka_db.get_left(), cfg_text_label.get_right(), buff=0.2, color=BLACK, path_arc=-0.2)
        arrow_cfg_to_mon = Arrow(cfg_group.get_right(), mon_group.get_left(), buff=0.2, color=BLACK)
        arrow_kafka_to_mon = Arrow(kafka_db, mon_circle, buff=0.2, color=BLACK)
        arrow_kafka_to_log = Arrow(kafka_db, log_circle, buff=0.2, color=BLACK)
        arrow_kafka_to_trace = Arrow(kafka_db, trace_circle, buff=0.2, color=BLACK)
        
        # ELK text for log
        elk_text = Text("ELK", font_size=20, color=BLACK).next_to(arrow_kafka_to_log.get_center(), UP, buff=0.01).shift(LEFT*0.5)

        self.play(
            Create(arrow_kafka_to_cfg),
            Create(arrow_cfg_to_mon),
            Create(arrow_kafka_to_mon),
            Create(arrow_kafka_to_log), Write(elk_text),
            Create(arrow_kafka_to_trace)
        )
        
        self.wait(3)