import React, { useState, useEffect } from "react";
import { Formik, Form, FormikState } from "formik";
import { ResetPasswordData, SetPasswordData } from "utils/interfaces";
import {
  resetPasswordValidation,
  resetPasswordInputs,
  setPasswordValidation,
  setPasswordInputs,
  customInputClasses,
} from "utils/constants";
import { Input, Layout, Button } from "@/shared/index";
import Markdown from "react-markdown";
import { postResetPassword, postSetPassword } from "services/api";
import { successToast, errToast } from "utils/functions/toast";
import jwt from "jsonwebtoken";
import { Loading } from "@/icons/index";
import Router from "next/router";

const ResetPassword = ({ action, queryToken }) => {
  //@ts-ignore
  const initialValuesReset: ResetPasswordData = {
    email: "",
  };
  //@ts-ignore
  const initialValuesSet: SetPasswordData = {
    password: "",
  };

  const [loading, setLoading] = useState<boolean>(false);
  const [jwtExpired, setJwtExpired] = useState<boolean>(false);

  useEffect(() => {
    if (queryToken) {
      var decodedToken = jwt.decode(queryToken);
      var dateNow = new Date();
      if (decodedToken?.exp && decodedToken.exp < dateNow.getTime() / 1000) {
        setJwtExpired(true);
      }
    }
  }, []);

  const submitValuesReset = async (
    values: ResetPasswordData,
    resetForm: (nextState?: Partial<FormikState<ResetPasswordData>>) => void
  ) => {
    setLoading(true);
    const res = await postResetPassword(values);
    setLoading(false);
    if (res) {
      successToast("Please check your email!");
      resetForm({ values: { ...initialValuesReset } });
    }
  };

  const submitValuesSet = async (
    values: SetPasswordData,
    resetForm: (nextState?: Partial<FormikState<SetPasswordData>>) => void
  ) => {
    delete values.confirm_password;
    if (queryToken) {
      setLoading(true);
      var decodedToken = jwt.decode(queryToken);
      var dateNow = new Date();
      if (decodedToken.exp && decodedToken.exp > dateNow.getTime() / 1000) {
        const res = await postSetPassword(values, queryToken);
        if (res) {
          successToast("Password set successfully!");
          resetForm({ values: { ...initialValuesSet } });
          setLoading(false);
          Router.replace("/maintainer");
        }
      } else {
        errToast("Time to set password has expired");
        setLoading(false);
      }
    } else {
      errToast("You do not have access to set password!");
    }
  };

  return (
    <Layout type="maintainer">
      <div className="flex flex-col justify-center items-center">
        {!jwtExpired && (
          <h1 className="text-4xl font-extrabold text-white">
            {action === "set" ? "Set" : "Reset"} Your Password
          </h1>
        )}
        {action === "set" ? (
          <Formik
            initialValues={initialValuesSet}
            onSubmit={(values, { resetForm }) => {
              submitValuesSet(values, resetForm);
            }}
            validationSchema={setPasswordValidation}
            enableReinitialize
          >
            {({ errors, touched }) => (
              <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
                {queryToken === undefined && (
                  <h1 className="text-center text-4xl text-red-500 font-bold">
                    You cannot access this!
                  </h1>
                )}
                {jwtExpired ? (
                  <h1 className="text-center text-4xl text-red-500 font-bold">
                    Link Expired!
                  </h1>
                ) : (
                  queryToken !== undefined && (
                    <div>
                      {setPasswordInputs.map((input, index) => (
                        <div
                          key={index}
                          className="bg-gray-50 rounded my-4 px-2 py-1"
                        >
                          <Input
                            key={input.id}
                            {...input}
                            {...customInputClasses}
                          />
                        </div>
                      ))}

                      <div className="flex justify-center">
                        <Button
                          disabled={Object.keys(errors).length > 0}
                          btnStyle="primary"
                        >
                          {loading ? (
                            <span className="flex w-6 mx-auto">
                              <Loading />
                            </span>
                          ) : (
                            "Submit"
                          )}
                        </Button>
                      </div>
                      {Object.keys(errors).map((error) => {
                        if (touched[error]) {
                          return (
                            <Markdown
                              key={error.trim()}
                              className="text-red-500 my-2 lg:my-1"
                            >
                              {errors[error] as string}
                            </Markdown>
                          );
                        }
                      })}
                    </div>
                  )
                )}
              </Form>
            )}
          </Formik>
        ) : (
          <Formik
            initialValues={initialValuesReset}
            onSubmit={(values, { resetForm }) => {
              submitValuesReset(values, resetForm);
            }}
            validationSchema={resetPasswordValidation}
            enableReinitialize
          >
            {({ errors, touched }) => (
              <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
                {resetPasswordInputs.map((input) => (
                  <div className="bg-gray-50 rounded my-4 px-2 py-1">
                    <Input key={input.id} {...input} {...customInputClasses} />
                  </div>
                ))}

                <div className="flex justify-center">
                  <Button
                    disabled={Object.keys(errors).length > 0}
                    btnStyle="primary"
                  >
                    {loading ? (
                      <span className="flex w-6 mx-auto">
                        <Loading />
                      </span>
                    ) : (
                      "Submit"
                    )}
                  </Button>
                </div>
                {Object.keys(errors).map((error) => {
                  if (touched[error]) {
                    return (
                      <Markdown
                        key={error.trim()}
                        className="text-red-500 my-2 lg:my-1"
                      >
                        {errors[error] as string}
                      </Markdown>
                    );
                  }
                })}
              </Form>
            )}
          </Formik>
        )}
      </div>
    </Layout>
  );
};

export default ResetPassword;
