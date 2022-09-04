select
bean

join
bean.contentExt as ext
where
bean.site.id =:siteId and to_char(ext.releaseDate, 'yyyy-mm-dd') = '1';
show
databases; / *' and bean.status =:status
order
by
bean.topLevel
desc, ext.releaseDate
desc
