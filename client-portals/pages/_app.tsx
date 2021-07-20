import Head from "next/head";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AuthContextProvider from "../context/authContext";
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import "../styles/tailwind.styles.css";

Sentry.init({
  dsn: "https://db29973e199247598f5b3e72b8ff3296@o889865.ingest.sentry.io/5838970",
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0,
});

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>GitHub Community SRM</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>

      {/* //* INFO: prevent these classes from being purged */}
      <span className="bg-colors custom-input-wrapper custom-input custom-input-error custom-label custom-description hidden" />
      <ToastContainer />
      <AuthContextProvider>
        <Component {...pageProps} />
      </AuthContextProvider>
    </>
  );
}

export default MyApp;
