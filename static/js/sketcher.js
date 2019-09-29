var s = {};
function sketch_section(container, size, cover, b, h, nt, nc, t_dia, c_dia) {
  if (size == "small") {
    b = b / 2;
    h = h / 2;
    nt = nt / 2;
    nc = nc / 2;
    t_dia = t_dia / 2;
    c_dia = c_dia / 2;
  }
  s[container] = Raphael(container, 500, 300);
  s[container].rect(0, 0, b, h);
  tx_offset = (b - 2 * cover + t_dia) / nt;
  cx_offset = (b - 2 * cover + c_dia) / nc;
  y_offset = cover;
  for (var i = 0; i < nt; i++) {
    s[container]
      .circle(i * tx_offset + cover, h - y_offset, t_dia)
      .attr("fill", "#ccc");
  }
  for (var i = 0; i < nc; i++) {
    s[container]
      .circle(i * cx_offset + cover, y_offset, c_dia)
      .attr("fill", "#ccc");
  }
}
