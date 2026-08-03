import { useState } from "react";
import PropTypes from "prop-types";

export default function PricingCard({
  planName,
  price,
  billingPeriod = "month",
  features,
  highlighted = false,
  onSelect,
}) {
  const [selected, setSelected] = useState(false);

  const handleSelect = () => {
    setSelected(true);
    onSelect?.(planName);
  };

  return (
    <div
      className={`relative w-72 rounded-xl bg-white p-6 shadow-md ${
        highlighted ? "ring-2 ring-blue-600" : "border border-gray-200"
      }`}
    >
      {highlighted && (
        <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold text-white">
          Most Popular
        </span>
      )}

      <h3 className="text-xl font-bold text-gray-900">{planName}</h3>
      <p className="mt-2 text-3xl font-extrabold text-gray-900">
        ${price}
        <span className="text-sm font-medium text-gray-500">
          /{billingPeriod}
        </span>
      </p>

      <ul className="mt-4 space-y-2 text-sm text-gray-700">
        {features.map((feature) => (
          <li key={feature} className="flex items-center gap-2">
            <span aria-hidden="true" className="text-blue-600">
              ✓
            </span>
            {feature}
          </li>
        ))}
      </ul>

      <button
        type="button"
        onClick={handleSelect}
        disabled={selected}
        aria-pressed={selected}
        className={`mt-6 w-full rounded-md px-4 py-2 font-medium transition-colors ${
          selected
            ? "cursor-default bg-green-600 text-white"
            : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
      >
        {selected ? "Selected ✓" : "Choose Plan"}
      </button>
    </div>
  );
}

PricingCard.propTypes = {
  planName: PropTypes.string.isRequired,
  price: PropTypes.number.isRequired,
  billingPeriod: PropTypes.string,
  features: PropTypes.arrayOf(PropTypes.string).isRequired,
  highlighted: PropTypes.bool,
  onSelect: PropTypes.func,
};
