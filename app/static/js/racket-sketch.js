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
  
  // Increase canvas size for a bigger sketch
  racketCanvas.width = 300;
  racketCanvas.height = 400;
  
  // Get the updated canvas size
  const canvasWidth = racketCanvas.width;
  const canvasHeight = racketCanvas.height;
  
  // Clear canvas
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);
  
  // Define racket shape parameters - make it fill almost the entire canvas
  const racketWidth = canvasWidth * 0.95;
  const racketHeight = canvasHeight * 0.98;
  const headWidth = racketWidth * 0.9;
  const headHeight = racketHeight * 0.75; // Stretch head vertically
  const handleLength = racketHeight * 0.04; // 90% shorter handle
  
  // Calculate center points - move it closer to the top to account for minimal handle
  const centerX = canvasWidth / 2;
  const headCenterY = canvasHeight * 0.45; // Move center slightly up
  
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
  ctx.lineWidth = 8; // Thicker frame
  
  // Draw head (ellipse)
  ctx.beginPath();
  ctx.ellipse(centerX, centerY, headWidth / 2, headHeight / 2, 0, 0, Math.PI * 2);
  ctx.stroke();
  
  // Draw handle (much shorter)
  const handleWidth = headWidth * 0.15;
  ctx.beginPath();
  ctx.moveTo(centerX - handleWidth / 2, centerY + headHeight / 2);
  ctx.lineTo(centerX - handleWidth / 2, centerY + headHeight / 2 + handleLength);
  ctx.lineTo(centerX + handleWidth / 2, centerY + headHeight / 2 + handleLength);
  ctx.lineTo(centerX + handleWidth / 2, centerY + headHeight / 2);
  ctx.stroke();
  
  // No grip patterns needed for very short handle
}

/**
 * Draws the string pattern inside the racket head
 */
function drawStringPattern(ctx, centerX, centerY, headWidth, headHeight, mainStrings, crossStrings) {
  const innerWidth = headWidth * 0.9; // Less space between strings and frame
  const innerHeight = headHeight * 0.9; // Less space between strings and frame
  
  // Draw vertical strings (main strings) - dark grey
  ctx.strokeStyle = '#333333'; // Darker grey for better visibility
  ctx.lineWidth = 2; // Thicker strings
  
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
  
  // Draw horizontal strings (cross strings) - red
  ctx.strokeStyle = '#D03030';
  
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