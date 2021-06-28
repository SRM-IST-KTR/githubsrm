import { useState } from "react";
import Link from "next/link";
import { Formik, Form } from "formik";
import Markdown from "react-markdown";

import { Section } from "../../";
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

const NewProject = () => {
  let [stage, setStage] = useState<number>(0);
  let [loading, setLoading] = useState<boolean>(false);

  const initialValues: Partial<NewMaintainerForm> = {};

  const submitValues = async (
    values: NewMaintainerForm,
    setErrors: (errors: Partial<NewMaintainerForm>) => void
  ) => {
    setLoading(true);
    try {
      if (await getUser(values.github_id)) {
        if (values.project_url.length > 0) {
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
          //@ts-ignore
          { ...parsedValues, tags: parsedTags },
          "alpha"
        );
      } else {
        setErrors({
          github_id: "**GitHub ID**: Invalid",
        } as Partial<NewMaintainerForm>);
        setLoading(false);
        return;
      }
    } catch (error) {
      console.log(error);
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
          <h1 className="text-4xl">Maintainer</h1>
          <h2 className="text-xl mt-2">alpha</h2>
        </div>

        <p className="text-right text-lg">
          Join us as a{" "}
          <Link href="/join-us/contributor">
            <a className="text-base-green font-bold hover:underline">
              Contributor
            </a>
          </Link>
        </p>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { setErrors }) =>
          submitValues(values as NewMaintainerForm, setErrors)
        }
        validationSchema={newMaintainerValidation}
      >
        {({ errors, touched }) => (
          <Form className="w-11/12 my-8 mx-auto">
            <div className="flex justify-evenly">
              <div className="w-4/12 flex flex-col items-center justify-between min-h-lg border-r-2">
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
                      } flex w-11/12 mx-auto flex-col`}
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

                <div className="w-11/12 mx-auto h-full pb-6 flex flex-col justify-end">
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

                <div className="w-11/12 mx-auto grid grid-cols-3 gap-x-10 items-center justify-center text-center">
                  <Link href="/join-us/maintainer/existing-project">
                    <a
                      type="button"
                      className="bg-base-teal py-3 rounded-lg text-white font-medium"
                    >
                      Existing Project?
                    </a>
                  </Link>
                  {stage == 0 ? (
                    <div />
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
                      disabled={Object.keys(errors).length > 0}
                      type="submit"
                      className={`${
                        Object.keys(errors).length > 0
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
