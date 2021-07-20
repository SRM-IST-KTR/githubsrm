import { useEffect, useState } from "react";

import { Member } from ".";
import { getTeam } from "../../services/api";
import { LoadingIcon } from "../../utils/icons";
import { MemberProps } from "../../utils/interfaces";

const Team = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);
  const [team, setTeam] = useState<MemberProps[]>();

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await getTeam();
        if (res) {
          setTeam(res);
        } else {
          setError(true);
        }
      } catch (error) {
        setError(true);
      }
      setLoading(false);
    })();
  }, []);

  return (
    <div>
      <h1 className="text-center text-3xl lg:text-5xl font-bold mb-10 text-base-black">
        Admins
      </h1>

      {loading ? (
        <div className="w-10 mx-auto text-base-smoke text-2xl">
          <LoadingIcon />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 text-center">
          {!error ? (
            team?.map((member) => <Member key={member.id} member={member} />)
          ) : (
            <>
              <span />
              <h3 className="text-center text-lg lg:text-2xl font-medium text-red-500 min-h-30">
                Error fetching team!
              </h3>
              <span />
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Team;
