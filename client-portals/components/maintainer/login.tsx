import React, { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import Markdown from "react-markdown";
import { MaintainerLoginData } from "../../utils/interfaces";
import {
  maintainerLoginValidation,
  maintainerLoginInputs,
  customInputClasses,
} from "../../utils/constants";
import { Input } from "../shared";
import Router from "next/router";
import { errToast, successToast } from "../../utils/functions/toast";
import { AuthContext } from "../../context/authContext";
import { useContext } from "react";
import Link from "next/link";
import { postMaintainerLogin } from "../../services/api";
import Footer from "../shared/footer";
import Loading from "../../utils/icons/loading";

const MaintainerLogin = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const authContext = useContext(AuthContext);

  //@ts-ignore
  const initialValues: MaintainerLoginData = {
    email: "",
    password: "",
  };

  const submitValues = async (
    values: MaintainerLoginData,
    resetForm: (nextState?: Partial<FormikState<MaintainerLoginData>>) => void
  ) => {
    setLoading(true);
    const res = await postMaintainerLogin(values);
    if (res) {
      authContext.decode();
      successToast("Logged In successfully!");
      Router.push("maintainer/dashboard");
      resetForm({ values: { ...initialValues } });
      setLoading(false);
    } else {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="min-h-screen p-14 bg-base-blue">
        <h1 className="flex justify-center text-4xl font-extrabold text-white">
          Maintainer Login
        </h1>

        <Formik
          initialValues={initialValues}
          onSubmit={(values, { resetForm }) => submitValues(values, resetForm)}
          validationSchema={maintainerLoginValidation}
        >
          {({ errors, touched }) => (
            <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
              {maintainerLoginInputs.map((input, index) => (
                <div
                  key={index}
                  className="border-2 border-gray-700 rounded my-4 p-4"
                >
                  <Input key={input.id} {...input} {...customInputClasses} />
                </div>
              ))}
              {Object.keys(errors).map((error) => {
                if (touched[error]) {
                  return (
                    <Markdown
                      key={error.trim()}
                      className="text-red-500 my-2 lg:my-2"
                    >
                      {errors[error] as string}
                    </Markdown>
                  );
                }
              })}
              <div className="flex flex-col items-center justify-center">
                <button
                  disabled={Object.keys(errors).length > 0}
                  type="submit"
                  className={`${
                    Object.keys(errors).length > 0
                      ? "cursor-not-allowed bg-opacity-70"
                      : "cursor-pointer"
                  } text-white bg-base-teal w-32 py-4 font-semibold rounded-lg`}
                >
                  {loading ? (
                    <span className="flex w-6 mx-auto">
                      <Loading />
                    </span>
                  ) : (
                    "Submit"
                  )}
                </button>
                <div className="text-md mt-5 hover:underline">
                  <Link href="/maintainer/reset-password/reset">
                    Forgot Password?
                  </Link>
                </div>
              </div>
            </Form>
          )}
        </Formik>
      </div>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default MaintainerLogin;
