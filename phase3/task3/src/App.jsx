import { useState } from "react";
import PricingCard from "./components/PricingCard.jsx";

const PLANS = [
  {
    planName: "Starter",
    price: 9,
    features: ["1 project", "Community support", "1 GB storage"],
  },
  {
    planName: "Pro",
    price: 29,
    features: ["Unlimited projects", "Priority support", "50 GB storage", "Team collaboration"],
    // highlighted: true,
  },
  {
    planName: "Enterprise",
    price: 99,
    features: ["Unlimited everything", "Dedicated support", "SSO & audit logs"],
  },
];

export default function App() {
  const [selectedPlan, setSelectedPlan] = useState(null);

  return (
    <div className="min-h-screen p-10">
      <h1 className="mb-8 text-center text-2xl font-bold text-gray-900">
        Choose your plan
      </h1>
      <div className="flex flex-wrap justify-center gap-6">
        {PLANS.map((plan) => (
          <PricingCard key={plan.planName} {...plan} onSelect={setSelectedPlan} />
        ))}
      </div>
      {selectedPlan && (
        <p className="mt-8 text-center text-gray-700">
          You selected the <strong>{selectedPlan}</strong> plan.
        </p>
      )}
    </div>
  );
}
