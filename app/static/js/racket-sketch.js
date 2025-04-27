/**
 * Racket String Pattern Visualization
 * Draws a visual representation of a tennis racket string pattern
 */
document.addEventListener('DOMContentLoaded', function() {
  const racketCanvas = document.getElementById('racket-canvas');
  if (!racketCanvas) return;
  
  const ctx = racketCanvas.getContext('2d');
  const pattern = racketCanvas.getAttribute('data-pattern');
  
  if (!pattern || !pattern.includes('x')) return;
  
  // Parse pattern (e.g., "16x19")
  const [mainStrings, crossStrings] = pattern.split('x').map(Number);
  
  // Set canvas size
  const canvasWidth = racketCanvas.width;
  const canvasHeight = racketCanvas.height;
  
  // Clear canvas
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  
  // Define racket shape parameters
  const racketWidth = canvasWidth * 0.8;
  const racketHeight = canvasHeight * 0.9;
  const headWidth = racketWidth * 0.7;
  const headHeight = racketHeight * 0.5;
  const handleLength = racketHeight * 0.4;
  
  // Calculate center points
  const centerX = canvasWidth / 2;
  const headCenterY = (canvasHeight - handleLength) / 2;
  
  // Draw racket outline
  drawRacketOutline(ctx, centerX, headCenterY, headWidth, headHeight, handleLength);
  
  // Draw string pattern
  drawStringPattern(ctx, centerX, headCenterY, headWidth, headHeight, mainStrings, crossStrings);
});

/**
 * Draws the outline of a tennis racket
 */
function drawRacketOutline(ctx, centerX, centerY, headWidth, headHeight, handleLength) {
  // Set styles for racket frame
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 6;
  
  // Draw head (ellipse)
  ctx.beginPath();
  ctx.ellipse(centerX, centerY, headWidth / 2, headHeight / 2, 0, 0, Math.PI * 2);
  ctx.stroke();
  
  // Draw handle
  const handleWidth = headWidth * 0.15;
  ctx.beginPath();
  ctx.moveTo(centerX - handleWidth / 2, centerY + headHeight / 2);
  ctx.lineTo(centerX - handleWidth / 2, centerY + headHeight / 2 + handleLength);
  ctx.lineTo(centerX + handleWidth / 2, centerY + headHeight / 2 + handleLength);
  ctx.lineTo(centerX + handleWidth / 2, centerY + headHeight / 2);
  ctx.stroke();
  
  // Draw grip patterns
  const gripLines = 6;
  const gripSpacing = handleLength / (gripLines + 1);
  ctx.lineWidth = 1;
  
  for (let i = 1; i <= gripLines; i++) {
    const y = centerY + headHeight / 2 + i * gripSpacing;
    ctx.beginPath();
    ctx.moveTo(centerX - handleWidth / 2, y);
    ctx.lineTo(centerX + handleWidth / 2, y);
    ctx.stroke();
  }
}

/**
 * Draws the string pattern inside the racket head
 */
function drawStringPattern(ctx, centerX, centerY, headWidth, headHeight, mainStrings, crossStrings) {
  // Set styles for strings
  ctx.strokeStyle = '#4287f5';
  ctx.lineWidth = 1.5;
  
  const innerWidth = headWidth * 0.85;
  const innerHeight = headHeight * 0.85;
  
  // Draw vertical strings (main strings)
  const mainSpacing = innerWidth / (mainStrings - 1);
  const mainStart = centerX - innerWidth / 2;
  
  for (let i = 0; i < mainStrings; i++) {
    const x = mainStart + i * mainSpacing;
    const startY = calculateYOnEllipse(x, centerX, centerY, innerWidth / 2, innerHeight / 2, true);
    const endY = calculateYOnEllipse(x, centerX, centerY, innerWidth / 2, innerHeight / 2, false);
    
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, endY);
    ctx.stroke();
  }
  
  // Draw horizontal strings (cross strings)
  const crossSpacing = innerHeight / (crossStrings - 1);
  const crossStart = centerY - innerHeight / 2;
  
  for (let i = 0; i < crossStrings; i++) {
    const y = crossStart + i * crossSpacing;
    const startX = calculateXOnEllipse(y, centerX, centerY, innerWidth / 2, innerHeight / 2, true);
    const endX = calculateXOnEllipse(y, centerX, centerY, innerWidth / 2, innerHeight / 2, false);
    
    ctx.beginPath();
    ctx.moveTo(startX, y);
    ctx.lineTo(endX, y);
    ctx.stroke();
  }
}

/**
 * Calculate Y coordinate on ellipse given X
 */
function calculateYOnEllipse(x, centerX, centerY, radiusX, radiusY, isUpper) {
  const normalizedX = (x - centerX) / radiusX;
  if (Math.abs(normalizedX) > 1) return centerY; // Outside ellipse
  
  const yOffset = radiusY * Math.sqrt(1 - normalizedX * normalizedX);
  return isUpper ? centerY - yOffset : centerY + yOffset;
}

/**
 * Calculate X coordinate on ellipse given Y
 */
function calculateXOnEllipse(y, centerX, centerY, radiusX, radiusY, isLeft) {
  const normalizedY = (y - centerY) / radiusY;
  if (Math.abs(normalizedY) > 1) return centerX; // Outside ellipse
  
  const xOffset = radiusX * Math.sqrt(1 - normalizedY * normalizedY);
  return isLeft ? centerX - xOffset : centerX + xOffset;
} 