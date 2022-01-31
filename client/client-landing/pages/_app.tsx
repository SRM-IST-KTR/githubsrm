import Head from "next/head";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import { Chat } from "../components/shared/crisp";

import "../styles/tailwind.styles.css";

if (process.env.NODE_ENV === "production") {
  Sentry.init({
    dsn: "https://db29973e199247598f5b3e72b8ff3296@o889865.ingest.sentry.io/5838970",
    integrations: [new Integrations.BrowserTracing()],
    tracesSampleRate: 1.0,
  });
  console.log(
    "\x1b[1m\x1b[32mServer in Production Mode. Sentry Enabled.\x1b[0m"
  );
} else {
  console.log(
    "\x1b[1m\x1b[33mServer in Development Mode. Disabling Sentry.\x1b[0m"
  );
}

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>GitHub Community SRM</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>

      {/* //* INFO: prevent these classes from being purged */}
      <span className="bg-colors custom-input-wrapper custom-input custom-input-error custom-label custom-description custom-option custom-option-label hidden" />
      <ToastContainer />
      <Chat />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
