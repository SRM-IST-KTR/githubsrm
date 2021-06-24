import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

interface types {
  email: string;
  githubid: string;
}

const Register = () => {
  const initialValues = {
    email: "",
    githubid: "",
  };

  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .trim()
      .required("No Email provided.")
      .email("Should be a valid email."),
    githubid: Yup.string().required("No githubid provided"),
  });

  const submitValues = (values: types) => {
    //api call here
    console.log(values);
  };

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={(values) => submitValues(values)}
      validationSchema={validationSchema}
    >
      {({ errors, touched }) => (
        <Form className="w-2/5">
          <div>
            <label htmlFor="email">Email</label>
            <Field
              type="email"
              name="email"
              placeholder="johndoe@mail.com"
              className={
                touched.email && errors.email
                  ? "border-solid border-2 border-red-800"
                  : "border-solid border-2 border-black"
              }
            />
            {errors.email && touched.email && (
              <div className="text-red-800 ">{errors.email}</div>
            )}
          </div>

          <div>
            <label htmlFor="githubid">Github Id</label>
            <Field
              type="githubid"
              name="githubid"
              placeholder="john-doe"
              className={
                touched.githubid && errors.githubid
                  ? "border-solid border-2 border-red-800"
                  : "border-solid border-2 border-black"
              }
            />
            {errors.githubid && touched.githubid && (
              <div className="text-red-800">{errors.githubid}</div>
            )}
          </div>

          <button type="submit" className="p-5">
            submit
          </button>
        </Form>
      )}
    </Formik>
  );
};

export default Register;
