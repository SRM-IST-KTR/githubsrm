// @ts-nocheck

import { useState } from "react";
import Link from "next/link";
import { Formik, Form, FormikState } from "formik";
import Markdown from "react-markdown";

import { Section } from "../..";
import { Input } from "../../../shared";
import {
  newMaintainerInputs,
  newMaintainerValidation,
  customInputClasses,
} from "../../../../utils/constants";
import { LoadingIcon } from "../../../../utils/icons";
import { NewMaintainerForm } from "../../../../utils/interfaces";
import { postMaintainer } from "../../../../services/api";
import { getRepo, getUser } from "../../../../services/validate";
import { successToast } from "../../../../utils/functions/toast";

const NewProject = () => {
  let [stage, setStage] = useState<number>(0);
  let [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: NewMaintainerForm = {
    name: "",
    email: "",
    github_id: "",
    srm_email: "",
    reg_number: "",
    branch: "",
    project_name: "",
    project_url: "",
    tags: "",
    description: "",
  };

  const submitValues = async (
    values: NewMaintainerForm,
    setErrors: (errors: Partial<NewMaintainerForm>) => void,
    resetForm: (nextState?: Partial<FormikState<NewMaintainerForm>>) => void
  ) => {
    setLoading(true);
    if (!values.project_visibility) {
      setErrors({
        project_visibility: "**Public Visibility:** Missing",
      } as Partial<NewMaintainerForm>);
      return;
    }
    values.project_visibility =
      values.project_visibility === "true"
        ? true
        : values.project_visibility === "false"
        ? false
        : null;

    if (await getUser(values.github_id)) {
      if (values.project_url?.length > 0) {
        const data = values.project_url.split("/");
        if (!(await getRepo(data[data.length - 2], data[data.length - 1]))) {
          setErrors({
            project_url: "**Public Repository URL:** Invalid",
          } as Partial<NewMaintainerForm>);
          setLoading(false);
          return;
        }
      }
      const { tags, ...parsedValues } = values;
      let parsedTags: string[] = tags
        .split(",")
        .filter((i) => i.trim().length > 0);
      const res = await postMaintainer(
        { ...parsedValues, tags: parsedTags },
        "alpha"
      );
      if (res) {
        successToast("Registered as a Maintainer!");
        setStage(0);
        resetForm({ values: { ...initialValues } });
        setLoading(false);
        return;
      }
    } else {
      setErrors({
        github_id: "**GitHub ID**: Invalid",
      } as Partial<NewMaintainerForm>);
      setLoading(false);
      return;
    }
    setLoading(false);
  };

  const changePage = (next: boolean) => {
    if (next) {
      if (stage !== newMaintainerInputs.length - 1) setStage(stage + 1);
    } else {
      if (stage !== 0) setStage(stage - 1);
    }
  };

  const errorInputId = (ids: string[], errors: string[]): boolean =>
    ids.some((id) => errors.includes(id));

  return (
    <div>
      <div>
        <div className="font-medium">
          <h1 className="text-2xl lg:text-4xl">Maintainer</h1>
          <h2 className="lg:text-xl lg:mt-2">
            Please fill the details correctly.
          </h2>
        </div>

        <p className="lg:text-right lg:text-lg mt-2 lg:mt-0">
          Interested in a project? Join us as a{" "}
          <Link href="/join-us/contributor">
            <a className="text-base-green font-bold hover:underline">
              Contributor
            </a>
          </Link>
          .
        </p>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { setErrors, resetForm }) =>
          submitValues(values as NewMaintainerForm, setErrors, resetForm)
        }
        validationSchema={newMaintainerValidation}
      >
        {({ errors, touched }) => (
          <Form className="w-full my-8 mx-auto">
            <div className="flex justify-evenly flex-col lg:flex-row max-w-6xl mx-auto">
              <div className="w-full lg:w-4/12 flex flex-col sm:flex-row lg:flex-col items-stretch lg:items-center justify-between lg:min-h-lg lg:border-r-2 lg:border-t-0 mb-12">
                {newMaintainerInputs.map((item, index) => (
                  <Section
                    key={item.section}
                    name={item.section}
                    description={item.description}
                    icon={item.icon}
                    isActive={stage === index}
                    setActive={() => setStage(index)}
                    onError={errorInputId(
                      item.inputs.map((i) => i.id),
                      Object.keys(errors).filter((i) => touched[i])
                    )}
                  />
                ))}
              </div>

              <div className="w-full max-w-3xl flex flex-col justify-between">
                <div>
                  {newMaintainerInputs.map((section, index) => (
                    <div
                      key={section.inputs[0].id}
                      className={`${
                        stage !== index ? "hidden" : ""
                      } flex w-11/12 mx-0 lg:mx-auto flex-col`}
                    >
                      {section.inputs.map((field) => (
                        <Input
                          onError={Object.keys(errors)
                            .filter((i) => touched[i])
                            .includes(field.id)}
                          key={field.id}
                          {...field}
                          {...customInputClasses}
                        />
                      ))}
                    </div>
                  ))}
                </div>

                <div className="w-11/12 text-sm md:text-base mx-auto h-full pb-6 flex flex-col justify-end">
                  {Object.keys(errors).map((error) => {
                    if (touched[error]) {
                      return (
                        <Markdown
                          key={error.trim()}
                          className="text-red-500 my-1"
                        >
                          {errors[error] as string}
                        </Markdown>
                      );
                    }
                  })}
                </div>

                <div className="w-11/12 mx-auto grid grid-rows-3 sm:grid-rows-none sm:grid-cols-3 lg:grid-rows-none lg:grid-cols-3 grid-flow-row lg:grid-flow-col gap-4 justify-items-auto">
                  <Link href="/join-us/maintainer/existing-project">
                    <a
                      type="button"
                      className="bg-base-teal py-3 rounded-lg text-white font-medium w-full text-center"
                    >
                      Existing Project?
                    </a>
                  </Link>
                  {stage == 0 ? (
                    <div className=" w-full py-3" />
                  ) : (
                    <button
                      type="button"
                      onClick={() => changePage(false)}
                      className="bg-base-smoke py-3 rounded-lg"
                    >
                      Back
                    </button>
                  )}

                  {stage !== newMaintainerInputs.length - 1 ? (
                    <button
                      type="button"
                      onClick={() => changePage(true)}
                      className="text-white bg-base-black py-3 font-semibold rounded-lg"
                    >
                      Next
                    </button>
                  ) : (
                    <button
                      disabled={Object.keys(errors).length > 0 || loading}
                      type="submit"
                      className={`${
                        Object.keys(errors).length > 0 || loading
                          ? "cursor-not-allowed bg-opacity-70"
                          : "cursor-pointer"
                      } text-white bg-base-green py-3 font-semibold rounded-lg`}
                    >
                      {!loading ? (
                        "Submit"
                      ) : (
                        <span className="flex w-6 mx-auto">
                          <LoadingIcon />
                        </span>
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default NewProject;
