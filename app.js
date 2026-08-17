const DEFAULT_RATE_BY_TYPE = {
  wood: 35,
  chainlink: 22,
  vinyl: 45,
  aluminum: 40,
};

const form = document.getElementById("estimator-form");
const formError = document.getElementById("form-error");
const resetBtn = document.getElementById("resetBtn");
const fenceType = document.getElementById("fenceType");
const materialRate = document.getElementById("materialRate");

const output = {
  adjustedLength: document.getElementById("outAdjustedLength"),
  materialCost: document.getElementById("outMaterialCost"),
  gateCost: document.getElementById("outGateCost"),
  laborCost: document.getElementById("outLaborCost"),
  subtotal: document.getElementById("outSubtotal"),
  taxAmount: document.getElementById("outTaxAmount"),
  grandTotal: document.getElementById("outGrandTotal"),
};

function setDefaultMaterialRate() {
  materialRate.value = DEFAULT_RATE_BY_TYPE[fenceType.value];
}

function toNumber(value) {
  return Number.parseFloat(value);
}

function toInt(value) {
  return Number.parseInt(value, 10);
}

function currency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function validate(values) {
  const invalid = Object.entries(values).find(([, value]) => Number.isNaN(value) || value < 0);
  if (invalid) {
    return "Please enter valid non-negative numbers in all fields.";
  }
  if (!Number.isInteger(values.gateCount)) {
    return "Gate count must be a whole number.";
  }
  return "";
}

function writeResult(result) {
  output.adjustedLength.textContent = `${result.adjustedLength.toFixed(2)} ft`;
  output.materialCost.textContent = currency(result.materialCost);
  output.gateCost.textContent = currency(result.gateCost);
  output.laborCost.textContent = currency(result.laborCost);
  output.subtotal.textContent = currency(result.subtotal);
  output.taxAmount.textContent = currency(result.taxAmount);
  output.grandTotal.textContent = currency(result.grandTotal);
}

function clearResult() {
  Object.values(output).forEach((field) => {
    field.textContent = "—";
  });
}

function calculate(values) {
  const adjustedLength = values.lengthFt * (1 + values.wastePct / 100);
  const materialCost = adjustedLength * values.materialRate;
  const gateCost = values.gateCount * values.gatePrice;
  const laborCost = adjustedLength * values.laborRateFt + values.gateCount * values.laborPerGate;
  const subtotal = materialCost + gateCost + laborCost;
  const taxAmount = subtotal * (values.taxPct / 100);
  const grandTotal = subtotal + taxAmount;

  return {
    adjustedLength,
    materialCost,
    gateCost,
    laborCost,
    subtotal,
    taxAmount,
    grandTotal,
  };
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  formError.textContent = "";

  const values = {
    lengthFt: toNumber(form.lengthFt.value),
    wastePct: toNumber(form.wastePct.value),
    materialRate: toNumber(form.materialRate.value),
    gateCount: toInt(form.gateCount.value),
    gatePrice: toNumber(form.gatePrice.value),
    laborRateFt: toNumber(form.laborRateFt.value),
    laborPerGate: toNumber(form.laborPerGate.value),
    taxPct: toNumber(form.taxPct.value),
  };

  const error = validate(values);
  if (error) {
    clearResult();
    formError.textContent = error;
    return;
  }

  const result = calculate(values);
  writeResult(result);
});

resetBtn.addEventListener("click", () => {
  form.reset();
  setDefaultMaterialRate();
  clearResult();
  formError.textContent = "";
});

fenceType.addEventListener("change", setDefaultMaterialRate);

setDefaultMaterialRate();
