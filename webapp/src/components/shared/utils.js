export function currencyFormatter(params) {
  return `$${params.value.toFixed(2)}`;
}

export const saleValueFormatter = function (params) {
  if (params){
    if (params.value) {
    var formatted = params.value.toFixed(2).replace(".", ",");
    if (formatted.indexOf("-") === 0) {
      return "-$" + formatted.slice(1);
    }
    return "$" + formatted;}
  }
};