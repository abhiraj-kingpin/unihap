import { CtaFooter } from "@/components/landing/cta-footer";
import { FeatureCards } from "@/components/landing/feature-cards";
import { FeatureShowcase } from "@/components/landing/feature-showcase";
import { Hero } from "@/components/landing/hero";
import { MetricsSection } from "@/components/landing/metrics-section";
import { WorkflowTimeline } from "@/components/landing/workflow-timeline";
import { SkipLink } from "@/components/common/skip-link";
import { Footer } from "@/components/layout/footer";
import { Header } from "@/components/layout/header";

export function LandingView() {
  return (
    <div className="flex min-h-screen flex-col bg-bg">
      <SkipLink />
      <Header />
      <main id="main-content">
        <Hero />
        <FeatureCards />
        <FeatureShowcase />
        <MetricsSection />
        <WorkflowTimeline />
        <CtaFooter />
      </main>
      <Footer />
    </div>
  );
}
