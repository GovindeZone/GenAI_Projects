import { createFileRoute } from "@tanstack/react-router";
import { useServerFn } from "@tanstack/react-start";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  MessageCircle, Mail, LayoutDashboard, Mic, Bot, Sparkles,
  Calendar, Cake, Newspaper, Wallet, Users, Bell, BookOpen,
  Megaphone, FileText, Database, BarChart3, Workflow, Activity, Cpu,
  Bot as ChatBot, FileSearch, AudioLines, PieChart, Network, Plug,
  Factory, ShoppingBag, Landmark, HeartPulse, Truck, Building2, GraduationCap, Briefcase,
  ArrowRight, Check, Linkedin, Facebook, Instagram, Youtube, Phone, MapPin,
  Home as HomeIcon, ShieldCheck, Wrench, UserCheck, Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { submitContact } from "@/lib/contact.functions";
import logo from "@/assets/ai-bro-logo-v2.png.asset.json";
import founderPhoto from "@/assets/founder-govind.jpg.asset.json";
import heroBg from "@/assets/hero-bg.jpg";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "AI Bro Solutions — Your AI Assistant for Work, Business & Life" },
      { name: "description", content: "Automate Tasks. Gain Insights. Grow Faster. AI Bro delivers Personal, Business & Community Assistants, AI automation, analytics and integrations." },
    ],
  }),
  component: Landing,
});

const nav = [
  { label: "Home", href: "#home" },
  { label: "Services", href: "#services" },
  { label: "Solutions", href: "#integrations" },
  { label: "Industries", href: "#industries" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

const CONTACT = {
  company: "AI Bro Solutions",
  emails: ["inquiries@aibro.sbs", "hello@aibro.sbs", "support@aibro.sbs"],
  phone: "+91 99520 83895",
  whatsapp: "+91 99520 83895",
  whatsappLink: "https://wa.me/919952083895",
  location: "Chennai, Tamil Nadu, India",
};

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <header className={`fixed top-0 inset-x-0 z-50 transition-all ${scrolled ? "pb-3" : "pb-5"}`}>
      {/* Announcement bar */}
      <div className="w-full bg-gradient-to-r from-primary/15 via-primary/25 to-primary/15 border-b border-primary/20 animate-pulse-glow">
        <div className="mx-auto max-w-7xl px-4 py-1.5 text-center text-[11px] md:text-xs font-semibold tracking-wide">
          <span className="gradient-text">✨ Transform Your Business Pain Points into AI-Powered Solutions</span>
        </div>
      </div>
      <div className={`mx-auto max-w-7xl px-4 ${scrolled ? "pt-3" : "pt-5"}`}>
        <div className={`flex items-center justify-between rounded-2xl px-4 md:px-6 py-3 ${scrolled ? "glass-card" : ""}`}>
          <a href="#home" className="flex items-center gap-2">
            <img src={logo.url} alt="AI Bro Solutions" className="h-10 w-auto" />
          </a>
          <nav className="hidden md:flex items-center gap-7">
            {nav.map(n => (
              <a key={n.href} href={n.href} className="text-sm text-muted-foreground hover:text-primary transition-colors">
                {n.label}
              </a>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <Button variant="hero" size="sm" asChild>
              <a href="#contact">Book a Free Demo</a>
            </Button>
            <button
              className="md:hidden glass-card w-9 h-9 grid place-items-center rounded-lg"
              aria-label="Toggle menu"
              onClick={() => setOpen(v => !v)}
            >
              <span className="text-lg leading-none">{open ? "✕" : "☰"}</span>
            </button>
          </div>
        </div>
        {open && (
          <div className="md:hidden mt-2 glass-card p-3 rounded-2xl flex flex-col">
            {nav.map(n => (
              <a key={n.href} href={n.href} onClick={() => setOpen(false)} className="px-3 py-2 text-sm hover:text-primary">
                {n.label}
              </a>
            ))}
          </div>
        )}
      </div>
    </header>
  );
}

const rotatingServices = [
  "Personal Assistant",
  "Business Assistant",
  "Community Assistant",
  "AI Chatbots",
  "WhatsApp Automation",
  "Dashboard & Analytics",
  "ERP & SAP Integration",
  "Voice AI Solutions",
  "OCR & Document Processing",
  "Workflow Automation",
  "Data Entry Automation",
];


function RotatingBanner({
  items,
  label,
  icon: Icon,
  interval = 2000,
}: { items: string[]; label: string; icon: any; interval?: number }) {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI(v => (v + 1) % items.length), interval);
    return () => clearInterval(t);
  }, [items, interval]);
  return (
    <div className="glass-card inline-flex items-center gap-3 px-5 py-3 rounded-2xl">
      <Icon className="w-5 h-5 text-primary shrink-0" />
      <span className="text-sm text-muted-foreground">{label}</span>
      <span key={i} className="text-base md:text-lg font-semibold gradient-text animate-fade-in">
        {items[i]}
      </span>
    </div>
  );
}

function FloatingIcon({ Icon, className, delay = "0s" }: { Icon: any; className: string; delay?: string }) {
  return (
    <div
      className={`absolute glass-card w-12 h-12 grid place-items-center rounded-2xl animate-float ${className}`}
      style={{ animationDelay: delay }}
    >
      <Icon className="w-5 h-5 text-primary" />
    </div>
  );
}

const offerings = [
  "AI Chatbots",
  "WhatsApp Automation",
  "Telegram Automation",
  "Dashboard & Analytics",
  "ERP Integration",
  "SAP Integration",
  "AI Powered Website Creation",
  "AI Video Creation",
  "AI Image Creation",
  "Workflow Automation",
  "Digital Marketing",
  "Data Entry Automation",
  "Voice AI Solutions",
];

const benefits = [
  "Save Time",
  "Reduce Cost",
  "Reduce Manual Work",
  "Increase Productivity",
  "Better Business Decisions",
  "Affordable AI Solutions",
  "Easy Integration",
  "Improve Data Accuracy",
  "Faster Decision Making",
  "Scalable Business Growth",
];

function VerticalTicker({ title, items, accent = "primary" }: { title: string; items: string[]; accent?: "primary" | "accent" }) {
  const [start, setStart] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setStart(v => (v + 1) % items.length), 2500);
    return () => clearInterval(t);
  }, [items.length]);
  const visible = Array.from({ length: 4 }, (_, k) => items[(start + k) % items.length]);
  const dotColor = accent === "accent" ? "bg-accent" : "bg-primary";
  return (
    <div className="glass-card p-5 rounded-2xl w-full">
      <div className="text-xs uppercase tracking-wider text-primary font-semibold mb-3">{title}</div>
      <div className="relative h-44 overflow-hidden">
        <ul className="space-y-2.5">
          {visible.map((label, k) => (
            <li
              key={`${start}-${k}`}
              className="flex items-center gap-2.5 text-sm font-medium animate-fade-in"
              style={{ animationDelay: `${k * 80}ms`, animationFillMode: "backwards" }}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${dotColor} shrink-0`} />
              <span className="truncate">{label}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function Hero() {
  return (
    <section id="home" className="relative pt-28 md:pt-32 pb-16 overflow-hidden">
      <div
        className="absolute inset-0 -z-10 opacity-40"
        style={{ backgroundImage: `url(${heroBg})`, backgroundSize: "cover", backgroundPosition: "center" }}
      />
      <div className="absolute inset-0 -z-10 grid-bg opacity-30" />
      <div className="absolute inset-0 -z-10" style={{ background: "var(--gradient-glow)" }} />

      <div className="mx-auto max-w-7xl px-4">
        <div className="grid lg:grid-cols-12 gap-6 items-center">
          {/* Left ticker */}
          <div className="lg:col-span-3 order-2 lg:order-1">
            <VerticalTicker title="What We Offer" items={offerings} />
          </div>

          {/* Center */}
          <div className="lg:col-span-6 order-1 lg:order-2 text-center">
            <div className="relative h-[200px] md:h-[240px] mx-auto">
              <div className="absolute inset-0 rounded-full" style={{ background: "var(--gradient-glow)" }} />
              <img
                src={logo.url}
                alt="AI Bro logo"
                width={240}
                height={240}
                className="relative z-10 mx-auto h-full w-auto object-contain animate-float drop-shadow-[0_25px_40px_rgba(255,193,7,0.25)]"
              />
              <FloatingIcon Icon={MessageCircle} className="left-2 md:left-8 top-8" delay="0.2s" />
              <FloatingIcon Icon={Mail} className="left-4 md:left-12 bottom-6" delay="0.6s" />
              <FloatingIcon Icon={LayoutDashboard} className="right-2 md:right-8 bottom-4" delay="1s" />
              <FloatingIcon Icon={Mic} className="right-4 md:right-12 top-10" delay="1.4s" />
            </div>


            <div className="mt-4 flex justify-center">
              <div className="glass-card px-6 py-3 rounded-2xl border border-primary/30 shadow-[0_0_30px_-10px_rgba(255,193,7,0.25)]">
                <span className="text-base md:text-lg font-bold text-foreground tracking-tight">
                  Your AI Assistant for Work, Business & Life
                </span>
              </div>
            </div>

            <p className="mt-3 text-xs md:text-sm font-semibold uppercase tracking-[0.18em] gradient-text">
              A Generative AI Architecture & Automation Company
            </p>

            <p className="mt-5 text-sm md:text-base text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Tell us your personal or business pain points, and let AI Bro deliver intelligent solutions that save time, cost, reduce effort, and drive growth.
            </p>

            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button variant="hero" size="lg" asChild>
                <a href="#contact">Book a Free Demo <ArrowRight className="w-4 h-4" /></a>
              </Button>
              <Button variant="glass" size="lg" asChild>
                <a href="#services">Explore Services</a>
              </Button>
            </div>

            <div className="mt-6 flex flex-wrap justify-center gap-x-6 gap-y-2 text-xs text-muted-foreground">
              <div className="flex items-center gap-2"><Check className="w-4 h-4 text-primary" /> 24×7 AI</div>
              <div className="flex items-center gap-2"><Check className="w-4 h-4 text-primary" /> 5× Faster</div>
              <div className="flex items-center gap-2"><Check className="w-4 h-4 text-primary" /> Easy Integration</div>
            </div>
          </div>

          {/* Right ticker */}
          <div className="lg:col-span-3 order-3">
            <VerticalTicker title="How We Can Help?" items={benefits} accent="accent" />
          </div>
        </div>
      </div>
    </section>
  );
}

function About() {
  return (
    <section id="about" className="py-20 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <div className="grid md:grid-cols-[260px_1fr] lg:grid-cols-[280px_1fr] gap-10 lg:gap-14 items-start">
          {/* Founder photo */}
          <div className="order-1 flex flex-col items-center md:items-start">
            <div className="w-full max-w-[200px] sm:max-w-[220px] md:max-w-[240px] lg:max-w-[260px] overflow-hidden rounded-2xl border border-primary/20 shadow-[0_20px_60px_-20px_rgba(0,0,0,0.5)] bg-background">
              <img
                src={founderPhoto.url}
                alt="Govindaraj Namachivayam - Founder & CEO, AI Bro Solutions"
                className="w-full h-auto object-cover"
              />
            </div>
            <div className="mt-4 text-center md:text-left">
              <div className="text-base font-semibold text-foreground">Govindaraj Namachivayam</div>
              <div className="text-xs text-muted-foreground">Founder & CEO, AI Bro</div>
            </div>
          </div>

          {/* About content */}
          <div className="order-2 text-center md:text-left">
            <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">About AI Bro</div>
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold">Your <span className="gradient-text">Smart AI Partner</span></h2>
            <p className="mt-5 text-muted-foreground text-base md:text-lg">
              AI Bro helps individuals and businesses automate repetitive work, gain insights from data,
              communicate smarter, and improve productivity using Artificial Intelligence.
            </p>
            <div className="glass-card p-6 mt-8 border-l-4 border-primary text-left">
              <p className="text-muted-foreground leading-relaxed">
                At <span className="text-foreground font-semibold">AI Bro</span>, our team brings together
                industry veterans, technology experts, and business consultants with decades of experience
                across finance, analytics, automation, and digital transformation. We focus on understanding
                your business pain points and delivering intelligent, sustainable, and economically viable
                solutions that create measurable business value.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function WhyChoose() {
  const items = [
    { icon: Activity, title: "Save Time", desc: "Automate repetitive tasks and reclaim hours every week." },
    { icon: Workflow, title: "Reduce Manual Work", desc: "Let AI handle the busywork so your team can focus." },
    { icon: Wallet, title: "Reduce Cost", desc: "Lower operational costs with intelligent automation." },
    { icon: BarChart3, title: "Increase Productivity", desc: "Get 5× faster output across business workflows." },
    { icon: PieChart, title: "Better Business Decisions", desc: "Real-time insights & analytics on tap." },
    { icon: Sparkles, title: "Affordable AI Solutions", desc: "Enterprise-grade AI without enterprise pricing." },
    { icon: Plug, title: "Easy Integration", desc: "Plugs into your existing stack in minutes." },
  ];
  return (
    <section id="why" className="py-24 relative">
      <div className="absolute inset-0 -z-10 opacity-60" style={{ background: "var(--gradient-glow)" }} />
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-14">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">The AI Bro Advantage</div>
          <h2 className="text-4xl md:text-5xl font-bold">Why Choose <span className="gradient-text">AI Bro?</span></h2>
          <p className="mt-4 text-muted-foreground max-w-xl mx-auto">
            Built to deliver real business value — from day one.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {items.map(({ icon: Icon, title, desc }) => (
            <div
              key={title}
              className="glass-card p-6 text-left hover:border-primary/50 hover:-translate-y-1 hover:shadow-[0_20px_60px_-20px_rgba(255,193,7,0.35)] transition-all group"
            >
              <div className="w-12 h-12 rounded-2xl gradient-bg grid place-items-center mb-4 group-hover:animate-pulse-glow">
                <Icon className="w-5 h-5 text-primary-foreground" />
              </div>
              <h3 className="font-semibold text-lg mb-1.5">{title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

type Svc = { icon: any; label: string };
function ServiceColumn({ title, kicker, items, description, featured }: { title: string; kicker: string; items: Svc[]; description?: string; featured?: boolean }) {
  return (
    <div
      className={`relative h-full flex flex-col p-7 rounded-xl border transition-all hover:-translate-y-1 ${
        featured
          ? "bg-gradient-to-br from-primary/15 via-background to-background border-primary/60 shadow-[0_20px_60px_-20px_rgba(255,193,7,0.45)] hover:shadow-[0_25px_70px_-15px_rgba(255,193,7,0.55)]"
          : "glass-card hover:border-primary/40"
      }`}
    >
      {featured && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-primary text-primary-foreground text-[10px] font-bold uppercase tracking-wider shadow-lg">
          Premium
        </div>
      )}
      <div className={`text-xs uppercase tracking-wider mb-2 ${featured ? "gradient-text font-bold" : "text-primary"}`}>{kicker}</div>
      <h3 className="text-2xl font-bold mb-3">{title}</h3>
      {description && <p className="text-sm text-muted-foreground mb-4 leading-relaxed">{description}</p>}
      <div className="space-y-2 mt-auto">
        {items.map(({ icon: Icon, label }) => (
          <div key={label} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors">
            <div className={`w-8 h-8 shrink-0 rounded-lg grid place-items-center ${featured ? "bg-primary/20 border border-primary/40" : "bg-primary/10 border border-primary/20"}`}>
              <Icon className="w-4 h-4 text-primary" />
            </div>
            <span className="text-sm">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Services() {
  const personal: Svc[] = [
    { icon: UserCheck, label: "Personal Assistant" },
    { icon: Sparkles, label: "Daily Greetings" },
    { icon: Cake, label: "Birthday Wishes" },
    { icon: Newspaper, label: "Daily News Updates" },
    { icon: Wallet, label: "Expense Tracking" },
    { icon: BookOpen, label: "Voice-to-Diary" },
    { icon: Calendar, label: "Meeting Scheduling" },
    { icon: Users, label: "Team Messaging" },
    { icon: Bell, label: "Transaction Alerts" },
  ];
  const business: Svc[] = [
    { icon: Megaphone, label: "Customer Campaigns" },
    { icon: FileText, label: "Invoice Generation" },
    { icon: Database, label: "ERP Data Retrieval" },
    { icon: BarChart3, label: "Stock Reports" },
    { icon: Cpu, label: "Data Entry Automation" },
    { icon: Sparkles, label: "Business Insights" },
    { icon: Activity, label: "KPI Monitoring" },
    { icon: Workflow, label: "Workflow Automation" },
  ];
  const solutions: Svc[] = [
    { icon: ChatBot, label: "AI Chatbots" },
    { icon: MessageCircle, label: "WhatsApp Automation" },
    { icon: Mail, label: "Telegram Automation" },
    { icon: FileSearch, label: "OCR & Document Processing" },
    { icon: AudioLines, label: "Voice AI" },
    { icon: LayoutDashboard, label: "Dashboard Development" },
    { icon: PieChart, label: "Data Analytics" },
    { icon: Network, label: "RPA Automation" },
    { icon: Plug, label: "Enterprise Integrations" },
    { icon: HomeIcon, label: "AI Website Creation" },
    { icon: Activity, label: "AI Video Creation" },
    { icon: Sparkles, label: "AI Image Creation" },
  ];
  const enterprise: Svc[] = [
    { icon: BookOpen, label: "AI Knowledge Assistant (RAG)" },
    { icon: FileSearch, label: "Enterprise Search & Document Intelligence" },
    { icon: Network, label: "Multi-Agent AI Systems" },
    { icon: Database, label: "AI-Powered ERP Assistant" },
    { icon: Cpu, label: "SAP AI Automation" },
    { icon: ShieldCheck, label: "Contract & Policy Intelligence" },
    { icon: FileText, label: "Invoice Processing & Approval Automation" },
    { icon: Briefcase, label: "AI Decision Support Systems" },
    { icon: BarChart3, label: "Predictive Analytics & Forecasting" },
    { icon: LayoutDashboard, label: "Executive AI Dashboards" },
    { icon: Wrench, label: "AI Copilots for Finance, HR & Procurement" },
    { icon: Bot, label: "Custom LLM Applications" },
  ];
  return (
    <section id="services" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-14 max-w-2xl mx-auto">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">What We Do</div>
          <h2 className="text-4xl md:text-5xl font-bold">Services built for <span className="gradient-text">every workflow</span></h2>
          <p className="mt-4 text-muted-foreground">From personal productivity to enterprise AI transformation.</p>
        </div>
        <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-6 items-stretch">
          <ServiceColumn
            kicker="For You"
            title="Personal AI Assistant"
            description="Automate your daily life with AI-powered assistants that help you stay organized, informed, and productive."
            items={personal}
          />
          <ServiceColumn
            kicker="For Teams"
            title="Business AI Assistant"
            description="Empower your business teams with intelligent automation that reduces manual work and improves decision-making."
            items={business}
          />
          <ServiceColumn
            kicker="For Businesses"
            title="AI Solutions"
            description="Modern AI solutions designed to automate customer engagement, business processes, reporting, and digital operations."
            items={solutions}
          />
          <ServiceColumn
            kicker="Premium · Enterprise"
            title="Enterprise AI Automation"
            description="Transform enterprise operations with next-generation AI systems that understand, reason, retrieve knowledge, automate workflows, and support strategic decisions."
            items={enterprise}
            featured
          />
        </div>
      </div>
    </section>
  );
}

function Industries() {
  const items = [
    { icon: Factory, name: "Manufacturing" },
    { icon: ShoppingBag, name: "Retail" },
    { icon: Landmark, name: "Finance" },
    { icon: HeartPulse, name: "Healthcare" },
    { icon: Truck, name: "Logistics" },
    { icon: Building2, name: "Real Estate" },
    { icon: GraduationCap, name: "Education" },
    { icon: Briefcase, name: "SMBs" },
  ];
  return (
    <section id="industries" className="py-24">
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-14">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">Industries</div>
          <h2 className="text-4xl md:text-5xl font-bold">Industries we <span className="gradient-text">serve</span></h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {items.map(({ icon: Icon, name }) => (
            <div key={name} className="glass-card p-6 text-center hover:border-primary/40 hover:-translate-y-1 transition-all group">
              <div className="w-14 h-14 mx-auto rounded-2xl gradient-bg grid place-items-center mb-4 group-hover:animate-pulse-glow">
                <Icon className="w-7 h-7 text-primary-foreground" />
              </div>
              <div className="font-semibold">{name}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function HowItWorks() {
  const steps = [
    { n: "01", title: "Tell AI Bro", desc: "Share your requirement in plain language — chat, voice or form." },
    { n: "02", title: "AI Analyzes", desc: "AI Bro understands your context, data and goals instantly." },
    { n: "03", title: "Solution Created", desc: "Automation, workflow or AI assistant gets configured." },
    { n: "04", title: "Instant Results", desc: "Get outcomes delivered — reports, messages, dashboards." },
  ];
  return (
    <section className="py-24 relative">
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-14">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">Process</div>
          <h2 className="text-4xl md:text-5xl font-bold">How AI Bro <span className="gradient-text">works</span></h2>
        </div>
        <div className="grid md:grid-cols-4 gap-6 relative">
          {steps.map((s, idx) => (
            <div key={s.n} className="glass-card p-6 relative">
              <div className="text-5xl font-bold gradient-text mb-3">{s.n}</div>
              <h3 className="font-semibold text-lg mb-2">{s.title}</h3>
              <p className="text-sm text-muted-foreground">{s.desc}</p>
              {idx < steps.length - 1 && (
                <ArrowRight className="hidden md:block absolute -right-3 top-1/2 w-6 h-6 text-primary z-10" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Integrations() {
  const logos = [
    "WhatsApp", "Telegram", "MS Teams", "Gmail", "Excel", "Power BI",
    "SAP", "Oracle", "Tally", "ServiceNow", "Jira", "Coupa",
  ];
  return (
    <section id="integrations" className="py-24">
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-12">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">Solutions & Integrations</div>
          <h2 className="text-4xl md:text-5xl font-bold">Plays well with <span className="gradient-text">your stack</span></h2>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
          {logos.map(l => (
            <div key={l} className="glass-card px-4 py-5 text-center text-sm font-medium hover:text-primary transition-colors">
              {l}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Metrics() {
  const m = [
    { v: "80%", l: "Reduction in Manual Work" },
    { v: "5×", l: "Faster Processing" },
    { v: "24×7", l: "AI Availability" },
    { v: "100%", l: "Digital Workflow" },
  ];
  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-4">
        <div className="glass-card p-10 md:p-14 relative overflow-hidden">
          <div className="absolute inset-0 -z-10 opacity-60" style={{ background: "var(--gradient-glow)" }} />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {m.map(x => (
              <div key={x.l}>
                <div className="text-5xl md:text-6xl font-bold gradient-text">{x.v}</div>
                <div className="text-sm text-muted-foreground mt-2">{x.l}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function Testimonials() {
  const t = [
    "AI Bro reduced our reporting effort by 70%.",
    "Invoice generation and reporting became fully automated.",
    "Excellent AI assistant for business operations.",
  ];
  return (
    <section className="py-24">
      <div className="mx-auto max-w-7xl px-4">
        <div className="text-center mb-14">
          <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">Loved by Teams</div>
          <h2 className="text-4xl md:text-5xl font-bold">What our <span className="gradient-text">customers say</span></h2>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {t.map(q => (
            <div key={q} className="glass-card p-7">
              <div className="text-primary text-3xl mb-3">"</div>
              <p className="text-lg">{q}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Contact() {
  return (
    <section id="contact" className="py-24">
      <div className="mx-auto max-w-7xl px-4">
        <div className="glass-card p-8 md:p-12 grid lg:grid-cols-2 gap-10">
          <div>
            <div className="text-sm text-primary font-semibold uppercase tracking-wider mb-3">Get Started</div>
            <h2 className="text-4xl md:text-5xl font-bold">Ready to work with <span className="gradient-text">AI Bro?</span></h2>
            <p className="mt-4 text-muted-foreground">Tell us your personal or business pain points. We'll show you how AI Bro can help in minutes.</p>
            <div className="mt-8 space-y-3 text-sm">
              {CONTACT.emails.map(e => (
                <div key={e} className="flex items-center gap-3">
                  <Mail className="w-4 h-4 text-primary" />
                  <a href={`mailto:${e}`} className="hover:text-primary">{e}</a>
                </div>
              ))}
              <div className="flex items-center gap-3">
                <Phone className="w-4 h-4 text-primary" />
                <a href={`tel:${CONTACT.phone.replace(/\s/g, "")}`} className="hover:text-primary">{CONTACT.phone}</a>
              </div>
              <div className="flex items-center gap-3">
                <MessageCircle className="w-4 h-4 text-primary" />
                <a href={CONTACT.whatsappLink} target="_blank" rel="noreferrer" className="hover:text-primary">WhatsApp: {CONTACT.whatsapp}</a>
              </div>
              <div className="flex items-center gap-3"><MapPin className="w-4 h-4 text-primary" /> {CONTACT.location}</div>
            </div>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button variant="hero" asChild><a href={`mailto:${CONTACT.emails[0]}`}>Email Us</a></Button>
              <Button variant="glass" asChild>
                <a href={CONTACT.whatsappLink} target="_blank" rel="noreferrer">
                  <MessageCircle className="w-4 h-4" /> WhatsApp Us
                </a>
              </Button>
            </div>
          </div>
          <ContactForm />
        </div>
      </div>
    </section>
  );
}

function ContactForm() {
  const send = useServerFn(submitContact);
  const [submitting, setSubmitting] = useState(false);
  const [loadedAt] = useState(() => Date.now());

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (submitting) return;
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: String(fd.get("name") || "").trim(),
      company: String(fd.get("company") || "").trim(),
      email: String(fd.get("email") || "").trim(),
      phone: String(fd.get("phone") || "").trim(),
      message: String(fd.get("message") || "").trim(),
      website: String(fd.get("website") || ""),
      ts: loadedAt,
    };
    if (!payload.name || !payload.email || !payload.message) {
      toast.error("Please fill in your name, email, and requirement.");
      return;
    }
    setSubmitting(true);
    const t = toast.loading("Sending your enquiry…");
    try {
      await send({ data: payload });
      toast.success("Thanks! Your AI Bro will reach out within 1 business day.", { id: t, duration: 6000 });
      e.currentTarget.reset();
    } catch (err) {
      console.error(err);
      toast.error("Couldn't send your enquiry. Please email inquiries@aibro.sbs directly.", { id: t });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="space-y-4" onSubmit={onSubmit}>
      <div className="grid sm:grid-cols-2 gap-4">
        <Field label="Name" name="name" required />
        <Field label="Company" name="company" />
        <Field label="Email" name="email" type="email" required />
        <Field label="Phone" name="phone" />
      </div>
      {/* Honeypot — hidden from real users, bots fill it in */}
      <div aria-hidden="true" style={{ position: "absolute", left: "-9999px", width: 1, height: 1, overflow: "hidden" }}>
        <label>
          Website
          <input type="text" name="website" tabIndex={-1} autoComplete="off" />
        </label>
      </div>
      <div>
        <label className="text-xs uppercase tracking-wider text-muted-foreground" htmlFor="message">Business Pain Point / Requirement</label>
        <textarea
          id="message"
          name="message"
          rows={5}
          required
          className="mt-1.5 w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 text-sm focus:outline-none focus:border-primary/60 transition-colors resize-none"
          placeholder="Tell us your personal or business pain points, and we'll deliver intelligent solutions..."
        />
      </div>
      <Button type="submit" variant="hero" size="lg" className="w-full" disabled={submitting}>
        {submitting ? (<><Loader2 className="w-4 h-4 animate-spin" /> Sending…</>) : (<>Book a Free Demo <ArrowRight className="w-4 h-4" /></>)}
      </Button>
    </form>
  );
}

function Field({ label, name, type = "text", required = false }: { label: string; name: string; type?: string; required?: boolean }) {
  return (
    <div>
      <label className="text-xs uppercase tracking-wider text-muted-foreground" htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        required={required}
        className="mt-1.5 w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 text-sm focus:outline-none focus:border-primary/60 transition-colors"
      />
    </div>
  );
}

function Footer() {
  return (
    <footer className="border-t border-white/10 pt-16 pb-8 mt-10">
      <div className="mx-auto max-w-7xl px-4">
        <div className="grid md:grid-cols-4 gap-10">
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <img src={logo.url} alt="AI Bro Solutions" className="h-9 w-auto" />
            </div>
            <div className="text-sm text-muted-foreground space-y-1 mb-5">
              <div className="font-semibold text-foreground">AI Bro Solutions</div>
              <div className="gradient-text font-semibold text-xs uppercase tracking-wider">A Generative AI Architecture & Automation Company</div>
              <div className="pt-2">Registered Company</div>
              <div>22-G Natham Link Road,</div>
              <div>Adjacent to OMR, SIPCOT IT Park</div>
              <div>Chennai-603103, Tamil Nadu, India</div>
            </div>
            <div className="flex items-center gap-3">
              {[Linkedin, Facebook, Instagram, Youtube].map((I, i) => (
                <a key={i} href="#" className="w-9 h-9 rounded-lg glass-card grid place-items-center hover:text-primary transition-colors">
                  <I className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>
          <div>
            <div className="font-semibold mb-3">Quick Links</div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {nav.map(n => <li key={n.href}><a href={n.href} className="hover:text-primary">{n.label}</a></li>)}
            </ul>
          </div>
          <div>
            <div className="font-semibold mb-3">Contact</div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {CONTACT.emails.map(e => (
                <li key={e}><a href={`mailto:${e}`} className="hover:text-primary">{e}</a></li>
              ))}
              <li>Phone: {CONTACT.phone}</li>
              <li>
                WhatsApp:{" "}
                <a href={CONTACT.whatsappLink} target="_blank" rel="noreferrer" className="hover:text-primary">
                  {CONTACT.whatsapp}
                </a>
              </li>
              <li>{CONTACT.location}</li>
            </ul>
          </div>
        </div>
        <div className="mt-12 pt-6 border-t border-white/10 text-center text-xs text-muted-foreground">
          © 2026 {CONTACT.company}. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}

function Landing() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Hero />
        <Services />
        <WhyChoose />
        <Industries />
        <HowItWorks />
        <Integrations />
        <Metrics />
        <Testimonials />
        <About />
        <Contact />
      </main>
      <Footer />
    </div>
  );
}
