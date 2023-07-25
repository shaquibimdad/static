export const metadata = {
  title: "Index",
  description: "Files",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        style={{
          backgroundColor: "#000000",
          color: "#fff",
          margin: 0,
          fontWeight: "bold",
        }}
      >
        Hello Bhai xD
        {children}
      </body>
    </html>
  );
}
