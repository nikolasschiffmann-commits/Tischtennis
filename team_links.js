function currentSeasonUrl(url, seasonStartMonth, teamId){
    const parsedUrl = new URL(url);

    if (parsedUrl.hostname !== "bttv.click-tt.de"){
        return url;
    }

    const now = new Date();
    const currentMonth = now.getMonth() + 1;
    const seasonStartYear = currentMonth >= seasonStartMonth
        ? now.getFullYear()
        : now.getFullYear() - 1;
    const seasonEnd = new Date(Date.UTC(
        seasonStartYear + 1,
        seasonStartMonth - 1,
        0
    ));
    const formatDate = date =>
        `${String(date.getUTCDate()).padStart(2, "0")}.${String(date.getUTCMonth() + 1).padStart(2, "0")}.${date.getUTCFullYear()}`;

    if (teamId){
        parsedUrl.searchParams.set("selectedTeamId", teamId);
    }
    parsedUrl.searchParams.set("searchTimeRangeFrom", `01.${String(seasonStartMonth).padStart(2, "0")}.${seasonStartYear}`);
    parsedUrl.searchParams.set("searchTimeRangeTo", formatDate(seasonEnd));
    return parsedUrl.toString();
}