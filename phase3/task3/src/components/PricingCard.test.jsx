import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import PricingCard from "./PricingCard.jsx";

const baseProps = {
  planName: "Pro",
  price: 29,
  features: ["Unlimited projects", "Priority support"],
};

describe("PricingCard", () => {
  it("renders the plan name, price, billing period, and features from props", () => {
    render(<PricingCard {...baseProps} />);

    expect(screen.getByText("Pro")).toBeInTheDocument();
    expect(screen.getByText("$29")).toBeInTheDocument();
    expect(screen.getByText("/month")).toBeInTheDocument();
    expect(screen.getByText("Unlimited projects")).toBeInTheDocument();
    expect(screen.getByText("Priority support")).toBeInTheDocument();
  });

  it("uses a custom billingPeriod when provided", () => {
    render(<PricingCard {...baseProps} billingPeriod="year" />);

    expect(screen.getByText("/year")).toBeInTheDocument();
  });

  it("shows a 'Most Popular' badge only when highlighted", () => {
    const { rerender } = render(<PricingCard {...baseProps} highlighted={false} />);
    expect(screen.queryByText("Most Popular")).not.toBeInTheDocument();

    rerender(<PricingCard {...baseProps} highlighted />);
    expect(screen.getByText("Most Popular")).toBeInTheDocument();
  });

  it("calls onSelect with the plan name and updates to a selected state on click", async () => {
    const onSelect = vi.fn();
    const user = userEvent.setup();
    render(<PricingCard {...baseProps} onSelect={onSelect} />);

    const button = screen.getByRole("button", { name: "Choose Plan" });
    await user.click(button);

    expect(onSelect).toHaveBeenCalledWith("Pro");
    expect(screen.getByRole("button", { name: "Selected ✓" })).toBeDisabled();
  });

  it("does not throw when onSelect is not provided", async () => {
    const user = userEvent.setup();
    render(<PricingCard {...baseProps} />);

    await user.click(screen.getByRole("button", { name: "Choose Plan" }));

    expect(screen.getByRole("button", { name: "Selected ✓" })).toBeInTheDocument();
  });
});
