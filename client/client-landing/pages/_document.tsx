import Document, { Html, Head, Main, NextScript } from "next/document";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  render() {
    return (
      <Html lang="en">
        <Head>
          <link
            rel="apple-touch-icon"
            sizes="180x180"
            href="/favicon/apple-touch-icon.png"
          />
          <link
            rel="icon"
            type="image/png"
            sizes="32x32"
            href="/favicon/favicon-32x32.png"
          />
          <link
            rel="icon"
            type="image/png"
            sizes="16x16"
            href="/favicon/favicon-16x16.png"
          />
          <link rel="manifest" href="/favicon/site.webmanifest" />

          <meta name="msapplication-TileColor" content="#0D1117" />
          <meta name="theme-color" content="#C9D1D9" />
          <meta charSet="utf-8" />
          <meta httpEquiv="Content-Type" content="text/html; charset=utf-8" />
          <meta name="title" content="GitHub Community SRM" />
          <meta
            name="description"
            content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
          />
          <meta
            name="keywords"
            content="github, githubsrm, github community srm, oss, open-source, srm, srmist, github campus partner, chennai"
          />
          <meta name="language" content="English" />
          <meta name="author" content="GitHub Community SRM" />
          <meta
            name="copyright"
            content="All rights reserved | GitHub Community SRM"
          />
          <meta httpEquiv="content-language" content="en" />

          <meta property="og:type" content="website" />
          <meta property="og:url" content="https://githubsrm.tech" />
          <meta property="og:title" content="GitHub Community SRM" />
          <meta
            property="og:description"
            content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
          />
          <meta property="og:image" content="/og.jpg" />

          <meta property="twitter:card" content="summary_large_image" />
          <meta property="twitter:url" content="https://githubsrm.tech" />
          <meta property="twitter:site" content="@githubsrm" />
          <meta
            property="twitter:title"
            content="Open Source Software (OSS) is the rock-solid foundation of the modern-day Internet. Right from the Android OS on your smartphone to the protocols that enable your IoT devices to communicate with each other, open-source software plays an important role in the software market share. With $66.05 Billion Open Source Services out in the market, it is imperative for developers to know this development ecosystem and be a part of the open-source revolution."
          />
          <meta
            property="twitter:description"
            content="Open Source Software (OSS) is the rock-solid foundation of the modern-day Internet. Right from the Android OS on your smartphone to the protocols that enable your IoT devices to communicate with each other, open-source software plays an important role in the software market share. With $66.05 Billion Open Source Services out in the market, it is imperative for developers to know this development ecosystem and be a part of the open-source revolution."
          />
          <meta property="twitter:image" content="/og.jpg" />

          <script
            async
            src="https://www.googletagmanager.com/gtag/js?id=G-3P9G0G50X8"
          />
          <script
            dangerouslySetInnerHTML={{
              __html: `
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());
                        gtag('config', 'G-3P9G0G50X8');
                      `,
            }}
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
