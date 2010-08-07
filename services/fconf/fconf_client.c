/**
 * Generated by fbus codegen(2010-08-01)
 */

#include "fbus_proxy.h"
#include "fconf_share.h"

#include "fconf_client.h"

typedef struct _PrivInfo
{
	FBusProxy* proxy;
	FConfOnChanged on_changed;
	void* on_changed_ctx;
}PrivInfo;

static Ret fconf_client_lock(FConf* thiz)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_LOCK);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		ret = fbus_parcel_get_int(parcel);
	}

	return ret;
}

static Ret fconf_client_unlock(FConf* thiz)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_UNLOCK);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		ret = fbus_parcel_get_int(parcel);
	}

	return ret;
}

static Ret fconf_client_remove(FConf* thiz, const char* xpath)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_REMOVE);
	fbus_parcel_write_string(parcel, xpath);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		ret = fbus_parcel_get_int(parcel);
	}

	return ret;
}

static Ret fconf_client_set(FConf* thiz, const char* xpath, const char* value)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_SET);
	fbus_parcel_write_string(parcel, xpath);
	fbus_parcel_write_string(parcel, value);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		ret = fbus_parcel_get_int(parcel);
	}

	return ret;
}

static Ret fconf_client_get(FConf* thiz, const char* xpath, char** value)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_GET);
	fbus_parcel_write_string(parcel, xpath);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		if((ret = fbus_parcel_get_int(parcel)) == RET_OK)
		{
			*value = (char*)fbus_parcel_get_string(parcel);
		}
	}

	return ret;
}

static Ret fconf_client_get_child_count(FConf* thiz, const char* xpath, int* count)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_GET_CHILD_COUNT);
	fbus_parcel_write_string(parcel, xpath);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		if((ret = fbus_parcel_get_int(parcel)) == RET_OK)
		{
			*count = fbus_parcel_get_int(parcel);
		}
	}

	return ret;
}

static Ret fconf_client_get_child(FConf* thiz, const char* xpath, int index, char** child)
{
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FBusParcel* parcel = fbus_proxy_get_parcel(priv->proxy);;
	return_val_if_fail(priv != NULL && priv->proxy != NULL && parcel != NULL, RET_FAIL);

	fbus_parcel_write_int(parcel, FCONF_GET_CHILD);
	fbus_parcel_write_string(parcel, xpath);
	fbus_parcel_write_int(parcel, index);

	if((ret = fbus_proxy_request(priv->proxy, parcel)) == RET_OK)
	{
		if((ret = fbus_parcel_get_int(parcel)) == RET_OK)
		{
			*child = (char*)fbus_parcel_get_string(parcel);
		}
	}

	return ret;
}

static Ret fconf_client_on_server_push(void* ctx, FBusPushTrigger trigger, FBusParcel* parcel)
{
	int type = 0;
	FConf* thiz = ctx;
	const char* path = NULL;
	const char* value = NULL;
	DECL_PRIV(thiz, priv);
	return_val_if_fail(thiz != NULL && parcel != NULL, RET_FAIL);

	if(priv->on_changed != NULL)
	{
		type = fbus_parcel_get_int(parcel);
		path = fbus_parcel_get_string(parcel);
		if(type != FCONF_CHANGED_BY_REMOVE)
		{
			value = fbus_parcel_get_string(parcel);
		}
		priv->on_changed(priv->on_changed_ctx, trigger == FBUS_TRIGGER_BY_SELF, type, path, value);
	}

	return RET_OK;
}

static Ret fconf_client_reg_changed_notify(FConf* thiz, FConfOnChanged on_changed, void* ctx)
{
	DECL_PRIV(thiz, priv);

	priv->on_changed = on_changed;
	priv->on_changed_ctx = ctx;

	if(priv->on_changed != NULL)
	{
		fbus_proxy_set_notify_listener(priv->proxy, fconf_client_on_server_push, thiz);
	}
	else
	{
		fbus_proxy_set_notify_listener(priv->proxy, NULL, NULL);
	}
	return RET_OK;
}


static void fconf_client_destroy(FConf* thiz)
{
	if(thiz != NULL)
	{
		DECL_PRIV(thiz, priv);
		fbus_proxy_destroy(priv->proxy);
		FTK_FREE(thiz);
	}
	return;
}

FConf* fconf_client_create(void)
{
	FConf* thiz = FTK_ZALLOC(sizeof(FConf) + sizeof(PrivInfo));

	if(thiz != NULL)
	{
		DECL_PRIV(thiz, priv);
		priv->proxy = fbus_proxy_create(FBUS_SERVICE_FCONF);
		thiz->lock = fconf_client_lock;
		thiz->unlock = fconf_client_unlock;
		thiz->remove = fconf_client_remove;
		thiz->set = fconf_client_set;
		thiz->get = fconf_client_get;
		thiz->get_child_count = fconf_client_get_child_count;
		thiz->get_child = fconf_client_get_child;
		thiz->reg_changed_notify = fconf_client_reg_changed_notify;
		thiz->destroy = fconf_client_destroy;
	}

	return thiz;
}