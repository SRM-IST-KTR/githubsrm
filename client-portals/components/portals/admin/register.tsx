import { Formik, Form, Field } from "formik";
import React, { useState, useEffect } from "react";
import { AdminRegisterData } from "../../../utils/interfaces";
import {
  adminRegisterValidation,
  adminRegisterInputs,
} from "../../../utils/constants";
import { Input } from "../../shared";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import AuthContext from "../../../services/auth-context";

const AdminRegister = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authToken, setAuthToken] = useState("");

  useEffect(() => {
    const storedUserLoggedInInformation = sessionStorage.getItem("isLoggedIn");

    if (storedUserLoggedInInformation === "1") {
      setIsLoggedIn(true);
    }
  }, []);

  const initialValues: { email: string; password: string } = {
    email: "",
    password: "",
  };

  const submitValues = (values: AdminRegisterData) => {
    instance
      .post("/admin/register", values, {
        headers: { Authorization: `Bearer ${authToken}` },
      })
      .then((res) => {
        successToast("Admin registered successfully!");
      })
      .catch((err) => {
        errToast("Oops! Some error occured");
      });
  };

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn: isLoggedIn,
      }}
    >
      {isLoggedIn && <p>register page -already logged in</p>}
      {!isLoggedIn && (
        <div className="min-h-screen p-14 bg-base-blue">
          <h1 className="flex justify-center text-4xl font-extrabold text-white">
            Admin Registration
          </h1>

          <Formik
            initialValues={initialValues}
            onSubmit={submitValues}
            validationSchema={adminRegisterValidation}
          >
            <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
              {adminRegisterInputs.map((input) => (
                <div className="border-2 border-gray-700 rounded my-4 p-4">
                  <Input key={input.id} {...input} />
                </div>
              ))}
              <Field
                onChange={(e) => setAuthToken(e.target.value)}
                className="border-2 border-gray-800 rounded-md p-3 mt-3"
                type="password"
                name="token"
                placeholder="Secret Key"
              />
              <div className="flex justify-center">
                <button
                  type="submit"
                  className="rounded-xl font-bold items-center my-3 bg-base-teal p-3"
                >
                  Register
                </button>
              </div>
            </Form>
          </Formik>
        </div>
      )}
    </AuthContext.Provider>
  );
};

export default AdminRegister;
