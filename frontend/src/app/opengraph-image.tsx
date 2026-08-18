import { ImageResponse } from "next/og";

export const alt = "UniHAP HITL Dashboard";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #00d9ff, #0099ff)",
        }}
      >
        <div style={{ fontSize: 76, fontWeight: 700, color: "#0a0e27" }}>UniHAP</div>
        <div style={{ fontSize: 28, color: "#0a0e27", marginTop: 18 }}>AI Product Review &amp; Curation</div>
      </div>
    ),
    { ...size },
  );
}
